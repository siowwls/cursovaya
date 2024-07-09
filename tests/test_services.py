import json
import unittest
from unittest.mock import Mock, patch

import pandas as pd

from src.services import search_transactions


class TestSearchTransactions(unittest.TestCase):

    @patch("pandas.read_excel")
    def test_search_transactions_empty(self, mock_read_excel):
        mock_read_excel.return_value = pd.DataFrame()
        result = search_transactions("Супермаркет", "mocked_file_path")
        self.assertEqual(result, json.dumps([], ensure_ascii=False))


if __name__ == "__main__":
    unittest.main()
