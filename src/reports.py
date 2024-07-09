import json
import logging
from datetime import datetime, timedelta

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


def spending_by_workday(transactions_1: pd.DataFrame, date: str = None) -> dict:
    """
    Функция выводит средние траты в рабочие и выходные дни
    """
    if date is None:
        date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    transactions_1["Дата операции"] = pd.to_datetime(
        transactions_1["Дата операции"], format="%d.%m.%Y %H:%M:%S"
    )
    three_months_ago = datetime.strptime(date, "%d.%m.%Y %H:%M:%S") - timedelta(days=90)
    filtered_transactions = transactions_1[
        transactions_1["Дата операции"] >= three_months_ago
    ]

    workdays = filtered_transactions[
        filtered_transactions["Дата операции"].dt.weekday < 5
    ]
    weekends = filtered_transactions[
        filtered_transactions["Дата операции"].dt.weekday >= 5
    ]

    avg_spending_workday = workdays["Сумма операции"].mean()
    avg_spending_weekend = weekends["Сумма операции"].mean()

    result_dict = {
        "Тип дня": ["Рабочий", "Выходной"],
        "Средние траты": [avg_spending_workday, avg_spending_weekend],
    }

    logging.info(f"Средние траты в рабочий день: {avg_spending_workday:.2f}")
    logging.info(f"Средние траты в выходной день: {avg_spending_weekend:.2f}")

    return json.dumps(result_dict, ensure_ascii=False, indent=2)


#
# transactions_1 = pd.read_excel("..\\data\\operations.xls")
# print(spending_by_workday(transactions_1, "03.01.2018 14:55:21"))
