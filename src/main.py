import pandas as pd

from src.reports import spending_by_workday
from src.services import search_transactions
from src.utils import (
    get_card_num,
    get_currency_rates,
    get_specific_stock_prices,
    top_transactions,
    welcome_message,
    write_dict,
)
from src.views import index_page


def main() -> None:
    """
    Главная функция, которая осуществляет все функции из модулей
    """
    user_date = input("Введите текущее время в формате %H:%M:%S: ")
    print(index_page(date_time=user_date))
    user_input = input("Введите запрос: ")
    print(search_transactions(user_input, "..\\data\\operations.xls"))
    option_date = input("Введите опциональную дату: ")
    transactions_1 = pd.read_excel("..\\data\\operations.xls")
    print(spending_by_workday(transactions_1, option_date))


if __name__ == "__main__":
    main()
