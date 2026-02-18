import tempfile
import unittest
from pathlib import Path

import pandas as pd

from helper_functions.convert_columns_to_lowercase import convert_columns_to_lowercase
from helper_functions.convert_text_file_into_dataframe import convert_text_file_into_dataframe
from helper_functions.do_mandatory_columns_exist import do_mandatory_columns_exist
from helper_functions.validate_tree_dbh_and_height_values import validate_tree_dbh_and_height_values


class TestDataImportPipelineIntegration(unittest.TestCase):
    def test_text_to_dataframe_validation_pipeline(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            txt_path = Path(tmp_dir) / "sample_input.txt"

            source_df = pd.DataFrame(
                {
                    "Plot": ["A1", "A2"],
                    "Year": [2020, 2021],
                    "Species": ["SP1", "SP2"],
                    "Tree Number": [1, 2],
                    "DBH": [10.1, 22.5],
                    "Height": [12.2, 15.0],
                }
            )
            source_df.to_csv(txt_path, sep="\t", index=False)

            imported_df = convert_text_file_into_dataframe(str(txt_path))

            self.assertIsNotNone(imported_df)
            self.assertEqual(len(imported_df), 2)
            self.assertTrue((Path(tmp_dir) / "sample_input.parquet").exists())

            lowered_df = convert_columns_to_lowercase(imported_df)

            self.assertTrue(do_mandatory_columns_exist(lowered_df))

            errors = validate_tree_dbh_and_height_values(lowered_df)
            self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
