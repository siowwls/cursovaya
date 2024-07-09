import json

from src.utils import (get_card_num, get_currency_rates,
                       get_specific_stock_prices, top_transactions,
                       welcome_message, write_dict)


def index_page(date_time: str) -> str:
    """
    Главная функция для отображения главной страницы
    """
    greeting = welcome_message(date_time)
    cards = get_card_num()
    currency = get_currency_rates()
    top = top_transactions()
    specific_tickers = ["AAPL", "AMZN", "GOOGL", "MSFT"]
    stock = get_specific_stock_prices(specific_tickers)
    result = {
        "Приветствие": greeting,
        "Карты": cards,
        "Курс валют": currency,
        "Топ 5 транзакций": top,
        "Стоимость акций": stock,
    }
    return json.dumps(result, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    transaction = write_dict("../data/operations.xls")
    user_date = input("Введите текущee время: ")
    print(index_page(date_time=user_date))
