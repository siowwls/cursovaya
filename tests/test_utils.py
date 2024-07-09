import unittest
from unittest.mock import Mock, patch

import pandas as pd

from src.utils import (get_card_num, get_currency_rates,
                       get_specific_stock_prices, top_transactions,
                       welcome_message, write_dict)


class SrcUtils(unittest.TestCase):

    @patch("utils.pd.read_excel")
    def test_write_dict(self, mock_read_excel):
        mock_data = {
            "Номер карты": [1234567890123456, 9876543210987654],
            "Сумма операции": [-1000, 2000],
            "Кэшбэк": [50, 0],
        }
        mock_df = pd.DataFrame(mock_data)

        mock_read_excel.return_value = mock_df

        expected_result = [
            {"Последние 4 цифры карты": "3456", "Сумма операции": 10.0, "Кэшбэк": 50},
            {"Последние 4 цифры карты": "7654", "Сумма операции": 20.0, "Кэшбэк": 0},
        ]

        result = get_card_num()
        self.assertEqual(result, expected_result)

    def test_welcome_message(self):
        result_morning = welcome_message("08:00:00")
        result_day = welcome_message("14:00:00")
        result_evening = welcome_message("20:00:00")
        result_night = welcome_message("02:00:00")

        self.assertEqual(result_morning, "Доброе утро")
        self.assertEqual(result_day, "Добрый день")
        self.assertEqual(result_evening, "Добрый вечер")
        self.assertEqual(result_night, "Доброй ночи")

    @patch("utils.write_dict")
    def test_top_transactions(self, mock_write_dict):
        mock_transactions = [
            {
                "Дата платежа": "01.06.2022",
                "Сумма платежа": -100,
                "Категория": "Еда",
                "Описание": "Ресторан",
            },
            {
                "Дата платежа": "02.06.2022",
                "Сумма платежа": -200,
                "Категория": "Шопинг",
                "Описание": "Магазин",
            },
        ]
        mock_write_dict.return_value = mock_transactions

        expected_result = [
            {
                "Дата платежа": "01.06.2022",
                "Сумма платежа": 100,
                "Категория": "Еда",
                "Описание": "Ресторан",
            },
            {
                "Дата платежа": "02.06.2022",
                "Сумма платежа": 200,
                "Категория": "Шопинг",
                "Описание": "Магазин",
            },
        ]

        result = top_transactions()
        self.assertEqual(result, expected_result)

    @patch("utils.requests.get")
    def test_get_currency_rates(self, mock_requests_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "Валюты": {"USD": {"Курс валюты": 75.0}, "EUR": {"Курс валюты": 85.0}}
        }
        mock_requests_get.return_value = mock_response

        expected_result = [
            {"Валюта": "USD", "Курс валюты": 75.0},
            {"Валюта": "EUR", "Курс валюты": 85.0},
        ]

        result = get_currency_rates()
        self.assertEqual(result, expected_result)

    @patch("utils.yf.Ticker")
    def test_get_specific_stock_prices(self, mock_ticker):
        mock_todays_data = Mock()
        mock_todays_data.empty = False
        mock_todays_data["High"].iloc.return_value = 500.0

        mock_ticker.return_value.history.return_value = mock_todays_data

        specific_tickers = ["AAPL", "AMZN"]

        expected_result = {
            "Цена акций": [
                {"Акция": "AAPL", "Цена акции": 500},
                {"Акция": "AMZN", "Цена акции": 500},
            ]
        }

        result = get_specific_stock_prices(specific_tickers)
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
