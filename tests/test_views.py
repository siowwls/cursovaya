import json
import unittest
from unittest.mock import Mock, patch

from src.utils import (
    get_card_num,
    get_currency_rates,
    get_specific_stock_prices,
    index_page,
    top_transactions,
    welcome_message,
    write_dict,
)


class TestIndexPage(unittest.TestCase):

    @patch("src.utils.welcome_message")
    @patch("src.utils.get_card_num")
    @patch("src.utils.get_currency_rates")
    @patch("src.utils.top_transactions")
    @patch("src.utils.get_specific_stock_prices")
    def test_index_page(
        self,
        mock_get_specific_stock_prices,
        mock_top_transactions,
        mock_get_currency_rates,
        mock_get_card_num,
        mock_welcome_message,
    ):
        mock_welcome_message.return_value = "Добрый день"
        mock_get_card_num.return_value = [
            {"Последние 4 цифры карты": "3456", "Сумма операции": 10.0, "Кэшбэк": 50},
            {"Последние 4 цифры карты": "7654", "Сумма операции": 20.0, "Кэшбэк": 0},
        ]
        mock_get_currency_rates.return_value = [
            {"currency": "USD", "rate": 75.0},
            {"currency": "EUR", "rate": 85.0},
        ]
        mock_top_transactions.return_value = [
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
        mock_get_specific_stock_prices.return_value = {
            "Цена акций": [
                {"Акция": "AAPL", "Цена акции": 500},
                {"Акция": "AMZN", "Цена акции": 600},
            ]
        }

        expected_result = {
            "Приветствие": "Добрый день",
            "Карты": [
                {
                    "Последние 4 цифры карты": "3456",
                    "Сумма операции": 10.0,
                    "Кэшбэк": 50,
                },
                {
                    "Последние 4 цифры карты": "7654",
                    "Сумма операции": 20.0,
                    "Кэшбэк": 0,
                },
            ],
            "Курс валют": [
                {"currency": "USD", "rate": 75.0},
                {"currency": "EUR", "rate": 85.0},
            ],
            "Топ 5 транзакций": [
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
            ],
            "Стоимость акций": {
                "Цена акций": [
                    {"Акция": "AAPL", "Цена акции": 500},
                    {"Акция": "AMZN", "Цена акции": 600},
                ]
            },
        }

        result = index_page(date_time="12:00:00")
        self.assertEqual(json.loads(result), expected_result)


if __name__ == "__main__":
    unittest.main()
