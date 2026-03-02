import sys
import importlib
import io
import json
import os
import tempfile
import time
import unittest
from contextlib import redirect_stdout
from typing import Any, cast
from unittest.mock import AsyncMock, MagicMock, mock_open, patch

import numpy as np
import pandas as pd

from helper_functions.check_dataframe_for_nan_values import check_dataframe_for_nan_values
from helper_functions.convert_columns_to_specific_types import convert_columns_to_specific_types
from helper_functions.do_mandatory_columns_exist import do_mandatory_columns_exist
from helper_functions.set_first_row_as_header import set_first_row_as_header
from helper_functions.validate_tree_dbh_and_height_values import validate_tree_dbh_and_height_values


def _as_float(value: object) -> float:
    return float(cast(Any, value))


class TestHelperEdgeCases(unittest.TestCase):
    def test_validate_boundaries_inclusive_and_exclusive(self):
        df = pd.DataFrame(
            {
                "dbh": [2.5, 99.9, 100.0, 2.49],
                "height": [1.3, 50.0, 10.0, 1.29],
            }
        )

        errors = validate_tree_dbh_and_height_values(df)

        self.assertEqual(len(errors), 2)
        bad_rows = sorted(err["index"] for err in errors)
        self.assertEqual(bad_rows, [2, 3])

    def test_validate_missing_required_columns_returns_empty(self):
        df = pd.DataFrame({"plot": ["A1"], "year": [2020]})
        self.assertEqual(validate_tree_dbh_and_height_values(df), [])

    def test_set_first_row_as_header_noop_when_expected_headers_present(self):
        df = pd.DataFrame(
            {
                "Plot": ["A1"],
                "SubPlot": [1],
                "Year": [2020],
                "Origin": ["Natural"],
                "TreeStatus": ["Alive"],
                "Species": ["SP1"],
                "Tree": [1],
                "DBH": [10.0],
                "Height": [12.0],
            }
        )

        with redirect_stdout(io.StringIO()):
            out = set_first_row_as_header(df)

        self.assertIs(out, df)
        self.assertEqual(list(out.columns), list(df.columns))

    def test_do_mandatory_columns_exist_is_case_insensitive(self):
        df = pd.DataFrame(
            {
                "PLOT": ["A1"],
                "YEAR": [2020],
                "SPECIES": ["SP1"],
                "TREE NUMBER": [1],
                "DBH": [10.0],
                "HEIGHT": [12.0],
            }
        )

        self.assertTrue(do_mandatory_columns_exist(df))

    def test_convert_columns_to_specific_types_converts_valid_preserves_invalid(self):
        df = pd.DataFrame(
            {
                "plot": [100, "A2"],
                "year": [2020, "bad"],
                "tree number": [1, "x"],
                "species": [123, "SP2"],
                "dbh": [10.56, "bad"],
                "height": [12.345, "oops"],
            }
        )

        out = convert_columns_to_specific_types(df)

        self.assertEqual(out.loc[0, "plot"], "100")
        self.assertEqual(out.loc[1, "year"], "bad")
        self.assertEqual(out.loc[1, "tree number"], "x")
        self.assertEqual(out.loc[0, "species"], 123)
        self.assertEqual(out.loc[1, "species"], "SP2")
        self.assertAlmostEqual(_as_float(out.loc[0, "dbh"]), 10.6, places=4)
        self.assertEqual(out.loc[1, "dbh"], "bad")
        self.assertAlmostEqual(_as_float(out.loc[0, "height"]), 12.34, places=4)
        self.assertEqual(out.loc[1, "height"], "oops")

    def test_check_dataframe_for_nan_values_reports_nan_and_type_issues(self):
        df = pd.DataFrame(
            {
                "year": [2020, None, "2021.5"],
                "tree number": [1, 2, "x"],
                "speccode": [101, "bad", 103],
                "dbh": [10.5, "bad", 11.2],
                "height": [12.0, 13.0, None],
            }
        )

        errors_detected, error_count, error_messages = check_dataframe_for_nan_values(df)

        self.assertTrue(errors_detected)
        self.assertEqual(error_count, 2)
        self.assertEqual(len(error_messages), 2)

        rows_with_errors = sorted(msg["index"] for msg in error_messages)
        self.assertEqual(rows_with_errors, [1, 2])

    def test_check_dataframe_for_nan_values_clean_data(self):
        df = pd.DataFrame(
            {
                "year": [2020, 2021],
                "tree number": [1, 2],
                "speccode": [101, 102],
                "dbh": [10.5, 11.0],
                "height": [12.0, 13.2],
            }
        )

        with redirect_stdout(io.StringIO()):
            errors_detected, error_count, error_messages = check_dataframe_for_nan_values(df)

        self.assertFalse(errors_detected)
        self.assertEqual(error_count, 0)
        self.assertEqual(error_messages, [])


class TestPerformanceAndRegression(unittest.TestCase):
    def _import_calculate_controller_module(self):
        with redirect_stdout(io.StringIO()):
            return importlib.import_module("controller.Calculate_Biomass_Controller")

    def test_validate_tree_dbh_and_height_performance_sanity(self):
        n = 20000
        df = pd.DataFrame(
            {
                "dbh": np.full(n, 25.0),
                "height": np.full(n, 18.0),
            }
        )

        start = time.perf_counter()
        errors = validate_tree_dbh_and_height_values(df)
        elapsed = time.perf_counter() - start

        self.assertEqual(errors, [])
        self.assertLess(elapsed, 10.0)

    def test_dbh_based_biomass_golden_regression(self):
        calc_mod = self._import_calculate_controller_module()
        Calculate_Biomass_Controller = calc_mod.Calculate_Biomass_Controller

        controller = Calculate_Biomass_Controller.__new__(Calculate_Biomass_Controller)
        controller.selected_components = ["Wood", "Bark", "Foliage", "Branch", "Crown", "Stem", "Total"]

        data = pd.DataFrame([{"dbh": 2.0}])
        row = data.iloc[0]
        species_params = {
            "bwood1": 2,
            "bwood2": 2,
            "bbark1": 3,
            "bbark2": 1,
            "bfoliage1": 1,
            "bfoliage2": 3,
            "bbranches1": 4,
            "bbranches2": 1,
        }

        controller._calculate_dbh_based_biomass(data, 0, row, species_params)

        golden = {
            "Wood (KG)": 8.0,
            "Bark (KG)": 6.0,
            "Foliage (KG)": 8.0,
            "Branch (KG)": 8.0,
            "Stem (KG)": 14.0,
            "Crown (KG)": 16.0,
            "Total (KG)": 30.0,
        }

        for col, expected in golden.items():
            self.assertAlmostEqual(_as_float(data.loc[0, col]), expected, places=4)

    def test_dbh_height_based_biomass_golden_regression(self):
        calc_mod = self._import_calculate_controller_module()
        Calculate_Biomass_Controller = calc_mod.Calculate_Biomass_Controller

        controller = Calculate_Biomass_Controller.__new__(Calculate_Biomass_Controller)
        controller.selected_components = ["Wood", "Bark", "Foliage", "Branch", "Crown", "Stem", "Total"]

        data = pd.DataFrame([{"dbh": 2.0, "height": 3.0}])
        row = data.iloc[0]
        species_params = {
            "bhwood1": 1,
            "bhwood2": 1,
            "bhwood3": 1,
            "bhbark1": 1,
            "bhbark2": 1,
            "bhbark3": 1,
            "bhbranches1": 1,
            "bhbranches2": 1,
            "bhbranches3": 1,
            "bhfoliage1": 1,
            "bhfoliage2": 1,
            "bhfoliage3": 1,
        }

        controller._calculate_dbh_height_based_biomass(data, 0, row, species_params)

        golden = {
            "Wood (KG)": 6.0,
            "Bark (KG)": 6.0,
            "Foliage (KG)": 6.0,
            "Branch (KG)": 6.0,
            "Stem (KG)": 12.0,
            "Crown (KG)": 12.0,
            "Total (KG)": 24.0,
        }

        for col, expected in golden.items():
            self.assertAlmostEqual(_as_float(data.loc[0, col]), expected, places=4)

    def test_dbh_height_based_biomass_skips_invalid_input(self):
        calc_mod = self._import_calculate_controller_module()
        Calculate_Biomass_Controller = calc_mod.Calculate_Biomass_Controller

        controller = Calculate_Biomass_Controller.__new__(Calculate_Biomass_Controller)
        controller.selected_components = ["Wood"]

        data = pd.DataFrame([{"dbh": "bad", "height": 3.0}, {"dbh": 2.0, "height": 0.0}])
        params = {"bhwood1": 1, "bhwood2": 1, "bhwood3": 1}

        controller._calculate_dbh_height_based_biomass(data, 0, data.iloc[0], params)
        controller._calculate_dbh_height_based_biomass(data, 1, data.iloc[1], params)

        self.assertNotIn("Wood (KG)", data.columns)

    def test_lower_column_names_handles_multiple_frames(self):
        calc_mod = self._import_calculate_controller_module()
        Calculate_Biomass_Controller = calc_mod.Calculate_Biomass_Controller

        controller = Calculate_Biomass_Controller.__new__(Calculate_Biomass_Controller)
        df1 = pd.DataFrame({"Plot": ["A1"], "DBH": [10]})
        df2 = pd.DataFrame({"Species": [101], "Height": [12]})

        controller._lower_column_names(df1, df2)

        self.assertEqual(list(df1.columns), ["plot", "dbh"])
        self.assertEqual(list(df2.columns), ["species", "height"])

    def test_calculate_single_component_zero_guard(self):
        calc_mod = self._import_calculate_controller_module()
        Calculate_Biomass_Controller = calc_mod.Calculate_Biomass_Controller
        controller = Calculate_Biomass_Controller.__new__(Calculate_Biomass_Controller)

        result = controller._calculate_single_component({"bwood1": 2, "bwood2": 2}, 0.0, "bwood1", "bwood2")
        self.assertEqual(result, 0.0)

    def test_export_results_to_text_file_success_state(self):
        calc_mod = self._import_calculate_controller_module()
        Calculate_Biomass_Controller = calc_mod.Calculate_Biomass_Controller

        controller = Calculate_Biomass_Controller.__new__(Calculate_Biomass_Controller)
        controller.view = MagicMock()

        with patch.object(calc_mod, "export_to_text_file", return_value=True):
            ok = controller.export_results_to_text_file("output.txt")

        self.assertTrue(ok)
        controller.view.show_success_dialog.assert_called_once()
        controller.view.show_error_dialog.assert_not_called()

    def test_export_results_to_text_file_failure_state(self):
        calc_mod = self._import_calculate_controller_module()
        Calculate_Biomass_Controller = calc_mod.Calculate_Biomass_Controller

        controller = Calculate_Biomass_Controller.__new__(Calculate_Biomass_Controller)
        controller.view = MagicMock()

        with patch.object(calc_mod, "export_to_text_file", return_value=False):
            ok = controller.export_results_to_text_file("output.txt")

        self.assertFalse(ok)
        controller.view.show_error_dialog.assert_called_once()
        controller.view.show_success_dialog.assert_not_called()

    def test_normalize_biomass_row_success_and_missing_fields(self):
        calc_mod = self._import_calculate_controller_module()
        Calculate_Biomass_Controller = calc_mod.Calculate_Biomass_Controller

        controller = Calculate_Biomass_Controller.__new__(Calculate_Biomass_Controller)
        controller.equation_type = "DBH-based"

        normalized = controller._normalize_biomass_row(
            {
                "Plot": "A1",
                "Year": 2020,
                "Species": 101,
                "Tree Number": 1,
                "DBH": 10.1,
                "Height": 12.2,
                "Wood (KG)": 2.0,
                "Bark (KG)": 1.0,
                "Foliage (KG)": 0.5,
                "Branch (KG)": 0.6,
                "Crown (KG)": 1.1,
                "Stem (KG)": 3.0,
                "Total (KG)": 4.1,
            }
        )

        self.assertEqual(normalized["plot"], "A1")
        self.assertEqual(normalized["year"], 2020)
        self.assertEqual(normalized["tree_number"], 1)
        self.assertEqual(normalized["coefficient_source"], "DBH-based")

        with self.assertRaises(ValueError):
            controller._normalize_biomass_row({"Plot": "A1"})


class TestDatabaseConfigBehavior(unittest.TestCase):
    @patch("data.database_config.pyodbc.drivers", return_value=["ODBC Driver 17 for SQL Server", "ODBC Driver 18 for SQL Server"])
    def test_get_sql_server_odbc_driver_picks_latest(self, _mock_drivers):
        from data.database_config import get_sql_server_odbc_driver

        self.assertEqual(get_sql_server_odbc_driver(), "ODBC Driver 18 for SQL Server")

    @patch("data.database_config.pyodbc.drivers", return_value=[])
    def test_get_sql_server_odbc_driver_raises_when_missing(self, _mock_drivers):
        from data.database_config import get_sql_server_odbc_driver

        with self.assertRaises(RuntimeError):
            get_sql_server_odbc_driver()

    @patch("data.database_config.glob.glob", side_effect=[["C:\\SQL\\DATA"], []])
    @patch.dict("os.environ", {"ProgramFiles": "C:\\PF", "ProgramFiles(x86)": "C:\\PF86"}, clear=False)
    def test_get_mssql_data_path_finds_first_match(self, _mock_glob):
        from data.database_config import get_mssql_data_path

        self.assertEqual(get_mssql_data_path(), "C:\\SQL\\DATA")


class TestBiomassCalculatorHelpers(unittest.TestCase):
    def _import_module_quiet(self, module_name: str):
        with redirect_stdout(io.StringIO()):
            return importlib.import_module(module_name)

    def test_reorder_by_species_code_sorts_rows(self):
        mod = self._import_module_quiet("helper_functions.Biomass_Calculator.reorder_by_species_code")
        df = pd.DataFrame({"species": [5, 1, 3], "dbh": [10, 11, 12]})

        out = mod.reorder_by_species_code(df)

        self.assertEqual(out["species"].tolist(), [1, 3, 5])

    def test_reorder_by_species_code_without_species_column_returns_input(self):
        mod = self._import_module_quiet("helper_functions.Biomass_Calculator.reorder_by_species_code")
        df = pd.DataFrame({"dbh": [10, 11, 12]})

        out = mod.reorder_by_species_code(df)

        self.assertIs(out, df)

    def test_extract_species_codes_from_local_storage_handles_mixed_values(self):
        mod = self._import_module_quiet(
            "helper_functions.Biomass_Calculator.extract_all_species_code_from_local_storage_json"
        )
        df = pd.DataFrame({"Species": ["101", "AB", "", None, 202]})

        out = mod.extract_all_species_codes_from_local_storage_json(df)

        self.assertEqual(out, [101, 202, "AB"])

    def test_extract_species_codes_from_two_json_files(self):
        mod = self._import_module_quiet(
            "helper_functions.Biomass_Calculator.extract_all_the_species_code_from_the_json_files"
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            p1 = os.path.join(tmp_dir, "a.json")
            p2 = os.path.join(tmp_dir, "b.json")
            with open(p1, "w", encoding="utf-8") as f:
                json.dump([{"SpecCommon": "Pine", "SpeciesCode": 101}, {"SpecCommon": "", "SpeciesCode": ""}], f)
            with open(p2, "w", encoding="utf-8") as f:
                json.dump([{"SpecCommon": "Spruce", "SpeciesCode": 102}, {"SpecCommon": "Pine"}], f)

            out = mod.extract_all_the_species_code_from_the_json_files(p1, p2)

        self.assertEqual(set(out), {"Pine", "Spruce", 101, 102})

    def test_create_hardwood_softwood_mapping(self):
        mod = self._import_module_quiet("helper_functions.Biomass_Calculator.create_hardwood_softwood_mapping")
        out = mod.create_hardwood_softwood_species_code_mapping([1, 2], [3])
        self.assertEqual(out, {1: "hardwood", 2: "hardwood", 3: "softwood"})

    def test_convert_json_to_dataframe_valid_and_invalid_path(self):
        mod = self._import_module_quiet("helper_functions.Biomass_Calculator.convert_json_to_dataframe")
        with tempfile.TemporaryDirectory() as tmp_dir:
            p = os.path.join(tmp_dir, "input.json")
            with open(p, "w", encoding="utf-8") as f:
                json.dump([{"a": 1}, {"a": 2}], f)

            ok_df = mod.convert_json_to_dataframe(p)
            bad_df = mod.convert_json_to_dataframe(os.path.join(tmp_dir, "missing.json"))

        self.assertEqual(ok_df.shape, (2, 1))
        self.assertTrue(bad_df.empty)

    def test_did_user_import_from_database_states(self):
        mod = self._import_module_quiet("helper_functions.Biomass_Calculator.did_user_import_from_database")
        cfg_mod = self._import_module_quiet("constants.Biomass_Config")

        with tempfile.TemporaryDirectory() as tmp_dir:
            selected_path = os.path.join(tmp_dir, "selected_database.json")

            with patch.object(cfg_mod.Biomass_Config, "SELECTED_DB_PATH", selected_path):
                with open(selected_path, "w", encoding="utf-8") as f:
                    f.write("{}")
                self.assertFalse(mod.did_user_import_from_database())

                with open(selected_path, "w", encoding="utf-8") as f:
                    f.write("{\"database\": \"test\"}")
                self.assertTrue(mod.did_user_import_from_database())

                os.remove(selected_path)
                self.assertFalse(mod.did_user_import_from_database())


class TestCsvImportHelper(unittest.TestCase):
    def _import_module_quiet(self, module_name: str):
        with redirect_stdout(io.StringIO()):
            return importlib.import_module(module_name)

    def test_csv_to_json_with_comma_delimiter_calls_data_manager(self):
        mod = self._import_module_quiet("data.import_dataset_helper")
        with tempfile.TemporaryDirectory() as tmp_dir:
            p = os.path.join(tmp_dir, "data.csv")
            with open(p, "w", encoding="utf-8") as f:
                f.write("Plot,Species\nA1,101\n")

            dm_instance = MagicMock()
            with patch.object(mod, "DataManager", return_value=dm_instance):
                with redirect_stdout(io.StringIO()):
                    mod.csv_to_json(p)

        dm_instance.set_all.assert_called_once_with([{"Plot": "A1", "Species": "101"}])
        dm_instance.save.assert_called_once()
        dm_instance.add_parameters.assert_called_once()

    def test_csv_to_json_with_tab_delimiter_calls_data_manager(self):
        mod = self._import_module_quiet("data.import_dataset_helper")
        with tempfile.TemporaryDirectory() as tmp_dir:
            p = os.path.join(tmp_dir, "data.txt")
            with open(p, "w", encoding="utf-8") as f:
                f.write("Plot\tSpecies\nA1\t101\n")

            dm_instance = MagicMock()
            with patch.object(mod, "DataManager", return_value=dm_instance):
                with redirect_stdout(io.StringIO()):
                    mod.csv_to_json(p)

        dm_instance.set_all.assert_called_once_with([{"Plot": "A1", "Species": "101"}])

    def test_csv_to_json_missing_file_no_data_manager_calls(self):
        mod = self._import_module_quiet("data.import_dataset_helper")
        with patch.object(mod, "DataManager") as dm_cls:
            with redirect_stdout(io.StringIO()):
                mod.csv_to_json("this_file_should_not_exist.csv")
        dm_cls.assert_not_called()


class TestPrintFileContent(unittest.TestCase):
    def test_print_file_content_missing_file_path(self):
        from helper_functions.print_file_content import print_file_content

        with redirect_stdout(io.StringIO()) as output:
            print_file_content("this_file_should_not_exist.txt")

        self.assertIn("Error: File not found", output.getvalue())

    def test_print_file_content_valid_file(self):
        from helper_functions.print_file_content import print_file_content

        with tempfile.TemporaryDirectory() as tmp_dir:
            p = os.path.join(tmp_dir, "sample.txt")
            with open(p, "w", encoding="utf-8") as f:
                f.write("hello world")
            with redirect_stdout(io.StringIO()) as output:
                print_file_content(p)

        self.assertIn("File processed successfully", output.getvalue())


class TestDataManagerCore(unittest.TestCase):
    def _import_module_quiet(self, module_name: str):
        with redirect_stdout(io.StringIO()):
            return importlib.import_module(module_name)

    def test_set_get_update_and_clear_cycle(self):
        dm_mod = self._import_module_quiet("data.data_manager")
        DataManager = dm_mod.DataManager

        with tempfile.TemporaryDirectory() as tmp_dir:
            local_path = os.path.join(tmp_dir, "localstorage.json")
            tree_path = os.path.join(tmp_dir, "treeparameters.json")
            selected_db_path = os.path.join(tmp_dir, "selected_database.json")
            metadata_path = os.path.join(tmp_dir, "metadata.json")

            with open(local_path, "w", encoding="utf-8") as f:
                json.dump([], f)

            with patch.object(DataManager, "_file_path", local_path), patch.object(
                DataManager, "_param_file_path", tree_path
            ), patch.object(DataManager, "_selected_db_path", selected_db_path), patch.object(
                DataManager, "_metadata_path", metadata_path
            ):
                DataManager._instance = None
                dm = DataManager()

                with redirect_stdout(io.StringIO()):
                    dm.set_all([{"SpecCommon": "Pine"}])
                self.assertEqual(dm.get_all(), [{"SpecCommon": "Pine"}])

                with redirect_stdout(io.StringIO()):
                    dm.update_entry(0, {"SpeciesCode": 101})
                self.assertEqual(dm.get_all()[0]["SpeciesCode"], 101)

                with redirect_stdout(io.StringIO()):
                    dm.clear()
                self.assertEqual(dm.get_all(), [])

                DataManager._instance = None

    def test_add_parameters_merges_matching_speccommon(self):
        dm_mod = self._import_module_quiet("data.data_manager")
        DataManager = dm_mod.DataManager

        with tempfile.TemporaryDirectory() as tmp_dir:
            local_path = os.path.join(tmp_dir, "localstorage.json")
            tree_path = os.path.join(tmp_dir, "treeparameters.json")
            selected_db_path = os.path.join(tmp_dir, "selected_database.json")
            metadata_path = os.path.join(tmp_dir, "metadata.json")

            with open(local_path, "w", encoding="utf-8") as f:
                json.dump([{"SpecCommon": "Pine"}, {"SpecCommon": "Unknown"}], f)
            with open(tree_path, "w", encoding="utf-8") as f:
                json.dump([{"SpecCommon": "Pine", "bwood1": 2.2, "bwood2": 1.8}], f)

            with patch.object(DataManager, "_file_path", local_path), patch.object(
                DataManager, "_param_file_path", tree_path
            ), patch.object(DataManager, "_selected_db_path", selected_db_path), patch.object(
                DataManager, "_metadata_path", metadata_path
            ):
                DataManager._instance = None
                dm = DataManager()
                with redirect_stdout(io.StringIO()):
                    dm.add_parameters()

                rows = dm.get_all()
                self.assertEqual(rows[0]["bwood1"], 2.2)
                self.assertNotIn("bwood1", rows[1])
                DataManager._instance = None

    def test_set_database_path_and_get_database_path_roundtrip(self):
        dm_mod = self._import_module_quiet("data.data_manager")
        DataManager = dm_mod.DataManager

        with tempfile.TemporaryDirectory() as tmp_dir:
            local_path = os.path.join(tmp_dir, "localstorage.json")
            tree_path = os.path.join(tmp_dir, "treeparameters.json")
            selected_db_path = os.path.join(tmp_dir, "selected_database.json")
            metadata_path = os.path.join(tmp_dir, "metadata.json")

            with open(local_path, "w", encoding="utf-8") as f:
                json.dump([], f)
            with open(selected_db_path, "w", encoding="utf-8") as f:
                json.dump({"server": "localhost", "database": "MyDb"}, f)

            with patch.object(DataManager, "_file_path", local_path), patch.object(
                DataManager, "_param_file_path", tree_path
            ), patch.object(DataManager, "_selected_db_path", selected_db_path), patch.object(
                DataManager, "_metadata_path", metadata_path
            ), patch.object(dm_mod, "get_sql_server_odbc_driver", return_value="ODBC Driver 18 for SQL Server"):
                DataManager._instance = None
                dm = DataManager()
                with redirect_stdout(io.StringIO()):
                    dm.set_database_path("MyDb")
                    db_path = dm.get_database_path()

                self.assertIn("Driver={ODBC Driver 18 for SQL Server};", db_path)
                self.assertIn("Server=localhost;", db_path)
                self.assertIn("Database=MyDb;", db_path)

                with open(metadata_path, "r", encoding="utf-8") as f:
                    meta = json.load(f)
                self.assertEqual(meta["db_name"], "MyDb")
                self.assertIn("db_path", meta)
                DataManager._instance = None


class TestCalculateBiomassControllerMethods(unittest.IsolatedAsyncioTestCase):
    def _import_calculate_controller_module(self):
        with redirect_stdout(io.StringIO()):
            return importlib.import_module("controller.Calculate_Biomass_Controller")

    def _new_controller(self):
        calc_mod = self._import_calculate_controller_module()
        controller_cls = calc_mod.Calculate_Biomass_Controller
        controller = controller_cls.__new__(controller_cls)
        return calc_mod, controller

    def test_get_database_selected_flag(self):
        _calc_mod, controller = self._new_controller()
        controller.is_database_selected = True
        self.assertTrue(controller.get_database_selected_flag())
        controller.is_database_selected = False
        self.assertFalse(controller.get_database_selected_flag())

    def test_extract_all_species_codes(self):
        _calc_mod, controller = self._new_controller()
        data = pd.DataFrame({"species": [101, 102, 101]})
        self.assertEqual(controller._extract_all_species_codes(data), [101, 102])
        self.assertEqual(controller._extract_all_species_codes(pd.DataFrame({"dbh": [10]})), [])

    def test_check_if_species_code_exists_within_the_json_files(self):
        _calc_mod, controller = self._new_controller()
        with tempfile.TemporaryDirectory() as tmp_dir:
            p1 = os.path.join(tmp_dir, "a.json")
            p2 = os.path.join(tmp_dir, "b.json")
            with open(p1, "w", encoding="utf-8") as f:
                json.dump([{"SpeciesCode": 101}], f)
            with open(p2, "w", encoding="utf-8") as f:
                json.dump([{"SpeciesCode": 202}], f)

            self.assertTrue(controller.check_if_species_code_exists_within_the_json_files(101, p1, p2))
            self.assertTrue(controller.check_if_species_code_exists_within_the_json_files(202, p1, p2))
            self.assertFalse(controller.check_if_species_code_exists_within_the_json_files(999, p1, p2))

    def test_create_hardwood_softwood_species_code_mapping(self):
        _calc_mod, controller = self._new_controller()
        mapping = controller._create_hardwood_softwood_species_code_mapping([1, 2], [3])
        self.assertEqual(mapping, {1: "hardwood", 2: "hardwood", 3: "softwood"})

    def test_lookup_and_get_species_parameters(self):
        _calc_mod, controller = self._new_controller()
        records = [{"speciescode": 101, "speccommon": "Pine"}, {"speciescode": 202, "speccommon": "Spruce"}]
        self.assertEqual(controller.lookup(records, 101)["speccommon"], "Pine")
        self.assertIsNone(controller.lookup(records, 999))

        params_df = pd.DataFrame(records)
        self.assertEqual(controller._get_species_parameters(params_df, 202)["speccommon"], "Spruce")

    async def test_on_calculate_biomass_click_success_and_failure(self):
        calc_mod, controller = self._new_controller()
        controller.view = MagicMock()
        controller.view.page = MagicMock()
        controller.view.disable_calculation_button = MagicMock()
        controller.view.enable_calculation_button = MagicMock()
        controller.view.show_results = MagicMock()
        controller.calculate_biomass = AsyncMock(side_effect=[True, False])

        class _FakeSpinner:
            def __init__(self, _page):
                self.hide = MagicMock()

            def show_dialog(self):
                return None

            async def simulate_progressive_loading(self, *_args, **_kwargs):
                return None

        event = type("Event", (), {"control": MagicMock()})()

        with patch.dict(sys.modules, {"widgets.Loading_Spinner_Widget": type("M", (), {"Loading_Spinner_Widget": _FakeSpinner})}), patch.dict(
            sys.modules, {"widgets.LogFileTxt": type("L", (), {"logger": MagicMock()})}
        ):
            await controller.on_calculate_biomass_click(event)
            await controller.on_calculate_biomass_click(event)

        self.assertEqual(controller.view.disable_calculation_button.call_count, 2)
        self.assertEqual(controller.view.enable_calculation_button.call_count, 2)
        controller.view.show_results.assert_called_once()

    def test_process_biomass_calculations_uses_code_name_and_mapping(self):
        calc_mod, controller = self._new_controller()
        controller.hardwood_and_softwood_species_code_mapping = [[{"SpeciesCode": "303", "bwood1": 1, "bwood2": 1}]]
        controller._calculate_row_biomass = MagicMock()

        local_data = pd.DataFrame({"species": [101, "jack pine", 303, "missing"], "dbh": [10, 10, 10, 10]})
        tree_params = pd.DataFrame([{"speciescode": 101, "speccommon": "Pine", "bwood1": 1, "bwood2": 1}])

        created_payload = [{"SpeciesCode": 202, "SpecCommon": "Jack Pine", "bwood1": 2, "bwood2": 1}]
        with patch("builtins.open", mock_open(read_data=json.dumps(created_payload))):
            controller._process_biomass_calculations(local_data, tree_params)

        self.assertEqual(controller._calculate_row_biomass.call_count, 3)

    def test_calculate_row_biomass_dispatch(self):
        _calc_mod, controller = self._new_controller()
        controller._calculate_dbh_based_biomass = MagicMock()
        controller._calculate_dbh_height_based_biomass = MagicMock()

        df = pd.DataFrame([{"dbh": 10, "height": 12}])
        row = df.iloc[0]

        controller.equation_type = "DBH-based"
        controller._calculate_row_biomass(df, 0, row, {})
        controller._calculate_dbh_based_biomass.assert_called_once()

        controller.equation_type = "DBH + Height-based"
        controller._calculate_row_biomass(df, 0, row, {})
        controller._calculate_dbh_height_based_biomass.assert_called_once()

    def test_dbh_height_formula_helpers(self):
        _calc_mod, controller = self._new_controller()
        self.assertAlmostEqual(controller._calculate_dbh_and_height_based_biomass_for_wood(2, 3, 1, 1, 1), 6.0)
        self.assertAlmostEqual(controller._calculate_dbh_and_height_based_biomass_for_bark(2, 3, 1, 1, 1), 6.0)
        self.assertAlmostEqual(controller._calculate_dbh_and_height_based_biomass_for_branch(2, 3, 1, 1, 1), 6.0)
        self.assertAlmostEqual(controller._calculate_dbh_and_height_based_biomass_for_foliage(2, 3, 1, 1, 1), 6.0)

    def test_individual_and_composite_component_paths(self):
        _calc_mod, controller = self._new_controller()
        controller.selected_components = ["Wood", "Bark", "Crown", "Stem", "Total"]
        controller._calculate_component_biomass = MagicMock()
        controller._calculate_crown_biomass = MagicMock()
        controller._calculate_stem_biomass = MagicMock()
        controller._calculate_total_biomass = MagicMock()

        df = pd.DataFrame([{"dbh": 10}])
        controller._calculate_individual_components(df, 0, {}, 10)
        controller._calculate_composite_components(df, 0, {}, 10)

        self.assertEqual(controller._calculate_component_biomass.call_count, 2)
        controller._calculate_crown_biomass.assert_called_once()
        controller._calculate_stem_biomass.assert_called_once()
        controller._calculate_total_biomass.assert_called_once()

    def test_calculate_component_and_composites(self):
        _calc_mod, controller = self._new_controller()
        df = pd.DataFrame([{"dbh": 2.0}])
        params = {
            "bwood1": 2,
            "bwood2": 2,
            "bbark1": 3,
            "bbark2": 1,
            "bfoliage1": 1,
            "bfoliage2": 3,
            "bbranches1": 4,
            "bbranches2": 1,
        }
        controller._calculate_component_biomass(df, 0, params, 2.0, "branches", "bbranches1", "bbranches2")
        self.assertEqual(df.loc[0, "Branch (KG)"], 8.0)

        controller._calculate_crown_biomass(df, 0, params, 2.0)
        controller._calculate_stem_biomass(df, 0, params, 2.0)
        controller._calculate_total_biomass(df, 0, params, 2.0)

        self.assertEqual(df.loc[0, "Crown (KG)"], 16.0)
        self.assertEqual(df.loc[0, "Stem (KG)"], 14.0)
        self.assertEqual(df.loc[0, "Total (KG)"], 30.0)

    def test_calculate_single_component_positive(self):
        _calc_mod, controller = self._new_controller()
        result = controller._calculate_single_component({"bwood1": 2, "bwood2": 2}, 3.0, "bwood1", "bwood2")
        self.assertEqual(result, 18.0)

    def test_save_results_calls_json_and_text(self):
        calc_mod, controller = self._new_controller()
        df = pd.DataFrame([{"species": 101}])
        controller._save_to_text_file = MagicMock()
        with patch.object(df, "to_json") as mock_to_json:
            controller._save_results(df)
        mock_to_json.assert_called_once_with(calc_mod.json_paths.BIOMASS_RESULTS_PATH, orient="records")
        controller._save_to_text_file.assert_called_once_with(df)

    def test_save_to_text_file_writes_header_and_rows(self):
        _calc_mod, controller = self._new_controller()
        df = pd.DataFrame([{"species": 101, "dbh": 10.0}, {"species": 202, "dbh": 11.0}])
        m = mock_open()
        with patch("builtins.open", m):
            controller._save_to_text_file(df)
        written = "".join(call.args[0] for call in m().write.call_args_list)
        self.assertIn("species\tdbh", written)
        self.assertIn("101\t10.0", written)
        self.assertIn("202\t11.0", written)

if __name__ == "__main__":
    unittest.main()
