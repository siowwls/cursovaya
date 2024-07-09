from src.utils import write_dict, get_card_num, welcome_message, top_transactions, get_currency_rates
from src.views import index_page
from src.services import search_transactions
from src.reports import spending_by_workday
import pandas as pd


def main() -> None:
    """
    Главная функция, которая осуществляет все функции из модулей
    """
    transactions_2 = write_dict("..\\data\\operations.xls")
    user_date = input("Введите текущую дату и время в формате YYYY-MM-DD HH:MM:SS: ")
    print(index_page(date_time=user_date, transactions=transactions_2))
    user_input = input("Введите запрос: ")
    print(search_transactions(user_input, "..\\data\\operations.xls"))
    option_date = input("Введите опциональную дату: ")
    transactions_1 = pd.read_excel("..\\data\\operations.xls")
    print(spending_by_workday(transactions_1, option_date))


if __name__ == "__main__":
    main()
