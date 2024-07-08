import json
# from src.logger import setup_logger
from src.utils import welcome_message, get_card_num, top_transactions, get_currency_rates, get_stock_prices, write_dict

# logger = setup_logger("views")


def index_page(date_time: str, transactions: list[dict]) -> str:
    """
   Главная функция для отображения главной страницы
   """
    # logger.info("Запуск главной страницы")
    greeting = welcome_message(date_time)
    cards = get_card_num(transactions)
    result = {"greeting": greeting, "cards": cards}
    return json.dumps(result, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    # logger.info("Запуск Веб-страницы")
    transaction = write_dict("../data/operations.xls")
    user_date = input("Введите текущую дату и время в формате YYYY-MM-DD MM:MM:SS")
    print(index_page(date_time=user_date))
