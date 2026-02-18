import unittest

import pandas as pd

from helper_functions.convert_columns_to_lowercase import convert_columns_to_lowercase
from helper_functions.do_mandatory_columns_exist import do_mandatory_columns_exist
from helper_functions.set_first_row_as_header import set_first_row_as_header
from helper_functions.validate_tree_dbh_and_height_values import validate_tree_dbh_and_height_values


class TestHelperFunctionsUnit(unittest.TestCase):
    def test_convert_columns_to_lowercase_returns_copy(self):
        original = pd.DataFrame({"Plot": ["A1"], "DBH": [10.5]})
        lowered = convert_columns_to_lowercase(original)

        self.assertEqual(list(lowered.columns), ["plot", "dbh"])
        self.assertEqual(list(original.columns), ["Plot", "DBH"])
        self.assertIsNot(original, lowered)

    def test_set_first_row_as_header_promotes_first_row_when_needed(self):
        df = pd.DataFrame(
            [
                ["Plot", "Year", "Species", "Tree Number", "DBH", "Height"],
                ["A1", 2020, "SP1", 1, 10.0, 12.0],
            ],
            columns=[0, 1, 2, 3, 4, 5],
        )

        out = set_first_row_as_header(df)

        self.assertEqual(
            list(out.columns),
            ["Plot", "Year", "Species", "Tree Number", "DBH", "Height"],
        )
        self.assertEqual(len(out), 1)

    def test_do_mandatory_columns_exist_passes_for_required_columns(self):
        df = pd.DataFrame(
            {
                "Plot": ["A1"],
                "Year": [2020],
                "Species": ["SP1"],
                "Tree Number": [1],
                "DBH": [10.2],
                "Height": [11.3],
            }
        )

        self.assertTrue(do_mandatory_columns_exist(df))

    def test_do_mandatory_columns_exist_raises_for_missing_columns(self):
        df = pd.DataFrame(
            {
                "Plot": ["A1"],
                "Year": [2020],
                "Species": ["SP1"],
                "DBH": [10.2],
            }
        )

        with self.assertRaises(ValueError):
            do_mandatory_columns_exist(df)

    def test_validate_tree_dbh_and_height_values_returns_errors(self):
        df = pd.DataFrame(
            {
                "dbh": ["bad", 150, 10],
                "height": [10, "oops", 0.5],
            }
        )

        errors = validate_tree_dbh_and_height_values(df)

        self.assertEqual(len(errors), 3)
        self.assertTrue(any(err["conversion_errors"] for err in errors))
        self.assertTrue(any(err["range_errors"] for err in errors))


if __name__ == "__main__":
    unittest.main()
