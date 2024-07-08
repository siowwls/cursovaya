from src.utils import write_dict, get_card_num, welcome_message, top_transactions
from src.views import index_page
from src.services import search_transact иions
from src.reports import report_to_file, spending_by_category


def main() -> None:
    """
    Главная функция, которая осуществляет все функци из модулей
    """
    transactions = write_dict(".../data/operations.xlsx")
    user_date = input("Введите текущую дату и время в формате YYYY-MM-DD HH:MM:SS")
    print(index_page(date_time=user_date))
    print("---------")


if __name__ == "__main__":
    main()
