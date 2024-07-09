from datetime import datetime
import requests
import pandas as pd
import json
from typing import Any, List


def write_dict(file_path: str) -> List[dict]:
    """
    Функция преобразовывает эксель-файл в словарь.
    """
    wine_reviews = pd.read_excel(file_path)
    file_dict = wine_reviews.to_dict(orient='records')
    return file_dict


def get_card_num(date: str) -> List[dict]:
    """
    Функция выводит информацию о картах: последние 4 цифры, сумма операции, кэшбэк.
    """
    cards = []
    transactions = write_dict(date)

    for element in transactions:
        card_number = str(element["Номер карты"])
        card_info = {
            "Последние 4 цифры карты": card_number[-4:],
            "Сумма операции": abs(element["Сумма операции"] / 100) if element["Сумма операции"] < 0 else element[
                                                                                                             "Сумма операции"] / 100,
            "Кэшбэк": element.get("Кэшбэк", 0)
        }
        cards.append(card_info)

    return cards


def welcome_message(date_time: str) -> str | None:
    """
    Функция возвращает приветствие в зависимости от времени.
    """
    current_time = datetime.strptime(date_time, "%H:%M:%S")
    if 6 <= current_time.hour < 12:
        return "Доброе утро"
    elif 12 <= current_time.hour < 18:
        return 'Добрый день'
    elif 18 <= current_time.hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def top_transactions(transactions: List[dict]) -> List[dict]:
    """
    Функция выводит топ-5 транзакций по сумме платежа.
    """
    sorted_transactions = sorted(transactions, key=lambda x: x['Сумма платежа'], reverse=True)[:5]
    top_transactions_list = []

    for transaction in sorted_transactions:
        top_transactions_list.append({
            "Дата платежа": transaction['Дата платежа'],
            "Сумма платежа": abs(transaction['Сумма платежа']),
            "Категория": transaction['Категория'],
            "Описание": transaction['Описание']
        })

    return top_transactions_list


def get_currency_rates() -> Any:
    """
    Функция выводит курсы валют.
    """
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        usd_rate = data['Valute']['USD']['Value']
        eur_rate = data['Valute']['EUR']['Value']

        currency_rates = [
            {"currency": "USD", "rate": usd_rate},
            {"currency": "EUR", "rate": eur_rate}
        ]

        return currency_rates
    else:
        return None


def get_stock_prices(symbol: str) -> Any:
    """
    Функция возвращает стоимость акций из S&P500.
    """
    api_key = "3R96U44IIIGFWZIJ"
    base_url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}'
    response = requests.get(base_url)
    data = response.json()
    price = data['Global Quote']['05. price']
    return price


def stocks_1() -> Any:
    """
    Функция возвращает json ответ, в котором есть название и цена акций
    """
    stocks = ['AAPL', 'AMZN', 'GOOGL', 'MSFT']
    stock_prices = []

    for stock in stocks:
        price = get_stock_prices(stock)
        stock_prices.append({"Акция": stock, "Цена": float(price)})

    json_data = json.dumps({"Цена акций": stock_prices}, indent=4)
    parsed_json = json.loads(json_data)

    pretty_json = json.dumps(parsed_json, ensure_ascii=False, indent=4)

    return pretty_json
