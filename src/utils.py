from datetime import datetime
import pandas as pd
import requests


def write_dict(file_path):
    """
    Функция преобразовывает эксель-файл в словарик
    """
    wine_reviews = pd.read_excel(file_path)
    file_dict = wine_reviews.to_dict(orient='records')
    return file_dict


#print(write_dict("..\\data\\operations.xls"))


def get_card_num(date):
    """
    Функция выводит словарик с данными по каждой карте: 4 последние цифры карты, сумма операции, кэшбэк
    """
    cards = []
    transactions = write_dict("..\\data\\operations.xls")

    for element in transactions:
        card_number = str(element["Номер карты"])
        card_info = {
            "Последние 4 цифры карты": card_number[-4:],
            "Сумма операции": abs(element["Сумма операции"] / 100)
            if element["Сумма операции"] < 0 else element["Сумма операции"] / 100, "Кэшбэк": element.get("Кэшбэк", 0)
        }
        cards.append(card_info)

    return cards


print(get_card_num(write_dict("..\\data\\operations.xls")))


def welcome_message(date_time: str) -> str | None:
    """
    Функция возвращает приветствие в зависимости от времени
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


# print(welcome_message("07:33:10"))


def top_transactions(transactions) -> list:
    """
    Функция выводит топ - 5 транзакций по сумме платежа
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


# print(top_transactions(write_dict("..\\data\\operations.xls")))


def get_currency_rates():
    """
    Функция выводит курс валют
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


# print(get_currency_rates())


def get_stock_prices():
    """
    Функция возвращает стоимость акций из S&P500.
    """
    api_key = "3R96U44IIIGFWZIJ"
    url = f'https://www.alphavantage.co/query?function=BATCH_Global_QUOTES&symbols=AAPL,AMZN,GOOGL,MSFT,TSLA&apikey={api_key}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        stock_prices = []
        for stock_data in data['Global Quote']:
            stock = stock_data['01. symbol']
            price = float(stock_data['05. price'])
            stock_prices.append({"stock": stock, "price": price})

        return {"Стоимость акций": stock_prices}
    else:
        return None

# print(get_stock_prices())
