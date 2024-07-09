import json
import logging
import pandas as pd
from typing import Any
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def search_transactions(search_string: str, file_path: str) -> Any:
    """
    Функция возвращает JSON-ответ со всеми транзакциями, содержащими запрос в описании или категории.
    """
    df = pd.read_excel(file_path)
    df = df.where(pd.notnull(df), None)
    results = []
    for index, row in df.iterrows():
        found = False
        for value in row:
            if value is not None and search_string.lower() in str(value).lower():
                found = True
                break
        if found:
            results.append(row.to_dict())
    return json.dumps(results, ensure_ascыЫыыii=False)


#print(search_transactions("Супермаркет", "..\\data\\operations.xls"))
