from datetime import datetime
from typing import Any, List

import pandas as pd
import requests
import yfinance as yf


def write_dict(file_path: str) -> List[dict]:
    """
    Функция преобразовывает эксель-файл в словарь.
    """
    wine_reviews = pd.read_excel(file_path)
    file_dict = wine_reviews.to_dict(orient="records")
    return file_dict


def get_card_num() -> List[dict]:
    """
    Функция выводит информацию о картах: последние 4 цифры, сумма операции, кэшбэк.
    """
    cards = []
    transactions = write_dict("..\\data\\operations.xls")

    for element in transactions:
        card_number = str(element["Номер карты"])
        card_info = {
            "Последние 4 цифры карты": card_number[-4:],
            "Сумма операции": (
                abs(element["Сумма операции"] / 100)
                if element["Сумма операции"] < 0
                else element["Сумма операции"] / 100
            ),
            "Кэшбэк": element.get("Кэшбэк", 0),
        }
        cards.append(card_info)

    return cards


def welcome_message(date_time: str) -> str | None:
    """
    Функция возвращает приветствие в зависимости от времени.
    """
    current_time = datetime.strptime(date_time.strip(), "%H:%M:%S")
    if 6 <= current_time.hour < 12:
        return "Доброе утро"
    elif 12 <= current_time.hour < 18:
        return "Добрый день"
    elif 18 <= current_time.hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


# print(welcome_message("19:49:10"))


def top_transactions() -> List[dict]:
    """
    Функция выводит топ-5 транзакций по сумме платежа.
    """
    transactions = write_dict("..\\data\\operations.xls")
    sorted_transactions = sorted(
        transactions, key=lambda x: x["Сумма платежа"], reverse=True
    )[:5]
    top_transactions_list = []

    for transaction in sorted_transactions:
        top_transactions_list.append(
            {
                "Дата платежа": transaction["Дата платежа"],
                "Сумма платежа": abs(transaction["Сумма платежа"]),
                "Категория": transaction["Категория"],
                "Описание": transaction["Описание"],
            }
        )

    return top_transactions_list


def get_currency_rates() -> Any:
    """
    Функция выводит курсы валют.
    """
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        usd_rate = data["Valute"]["USD"]["Value"]
        eur_rate = data["Valute"]["EUR"]["Value"]

        currency_rates = [
            {"currency": "USD", "rate": usd_rate},
            {"currency": "EUR", "rate": eur_rate},
        ]

        return currency_rates
    else:
        return None


def get_specific_stock_prices(tickers: list) -> dict:
    """
    Получает данные о максимальной цене за день для заданных акций.
    """
    stock_prices = []

    for tickerr in tickers:
        todays_data = yf.Ticker(tickerr).history(period="1d")
        if not todays_data.empty:
            high_price = todays_data["High"].iloc[0]
            stock_prices.append({"Акция": tickerr, "Цена акции": round(high_price)})

    return {"Цена акций": stock_prices}


# specific_tickers = ['AAPL', 'AMZN', 'GOOGL', 'MSFT']
#
# result = get_specific_stock_prices(specific_tickers)
# print(result)
