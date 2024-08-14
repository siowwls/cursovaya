import json
import unittest
from typing import Any
from unittest.mock import patch

import pandas as pd

from src.reports import spending_by_workday


class TestSpendingByWorkday(unittest.TestCase):

    @patch("reports.pd.read_excel")
    def test_spending_by_workday(self, mock_read_excel: Any) -> None:
        mock_data = {
            "Дата операции": [
                "01.06.2022 12:00:00",
                "02.06.2022 12:00:00",
                "03.06.2022 12:00:00",
            ],
            "Сумма операции": [100, 200, 150],
        }
        mock_df = pd.DataFrame(mock_data)
        mock_read_excel.return_value = mock_df
        expected_result = {
            "Тип дня": ["Рабочий", "Выходной"],
            "Средние траты": [125.0, 200.0],
        }
        result = spending_by_workday(mock_df, date="03.06.2022 12:00:00")
        self.assertEqual(
            result, json.dumps(expected_result, ensure_ascii=False, indent=2)
        )


if __name__ == "__main__":
    unittest.main()
