import pandas as pd
import logging
from datetime import datetime, timedelta
from functools import wraps

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def report_to_file(file_name="report.txt"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(file_name, "w") as file:
                file.write(result.to_string())
            logger.info(f"Результат отчета записан в файл: {file_name}")
            return result

        return wrapper

    return decorator


@report_to_file("spending_report.txt")
def spending_by_category(transactions_df: pd.DataFrame, category: str, date: str = None) -> pd.DataFrame:
    """
    Функция для получения трат по заданной категории за последние три месяца от переданной даты
    """
    if date is None:
        date = datetime.now().strftime('%d.%m.%Y')
        return date
    else:
        transactions_df['Дата операции'] = pd.to_datetime(transactions_df['Дата операции'], format='%d.%m.%Y %H:%M:%S')
        three_months_ago = datetime.strptime(date, '%d.%m.%Y') - timedelta(days=90)
        filtered_transactions = transactions_df[(transactions_df['Категория'] == category) &
                                                (transactions_df['Дата операции'] >= three_months_ago)]
        return filtered_transactions
