import decimal
import importlib
import io
import json
import os
import sys
import tempfile
import types
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, mock_open, patch

import pandas as pd

from helper_functions.convert_columns_to_lowercase import convert_columns_to_lowercase
from helper_functions.convert_text_file_into_dataframe import convert_text_file_into_dataframe
from helper_functions.do_mandatory_columns_exist import do_mandatory_columns_exist
from helper_functions.validate_tree_dbh_and_height_values import validate_tree_dbh_and_height_values


class TestPipelineStatesIntegration(unittest.TestCase):
    def _write_tab_file(self, directory: str, filename: str, df: pd.DataFrame) -> Path:
        file_path = Path(directory) / filename
        df.to_csv(file_path, sep="\t", index=False)
        return file_path

    def test_state_success_valid_rows(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            txt_path = self._write_tab_file(
                tmp_dir,
                "valid.txt",
                pd.DataFrame(
                    {
                        "Plot": ["A1", "A2"],
                        "Year": [2020, 2021],
                        "Species": ["SP1", "SP2"],
                        "Tree Number": [1, 2],
                        "DBH": [8.0, 22.5],
                        "Height": [12.2, 15.0],
                    }
                ),
            )

            imported = convert_text_file_into_dataframe(str(txt_path))
            lowered = convert_columns_to_lowercase(imported)

            self.assertTrue(do_mandatory_columns_exist(lowered))
            self.assertEqual(validate_tree_dbh_and_height_values(lowered), [])

    def test_state_missing_mandatory_column_raises(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            txt_path = self._write_tab_file(
                tmp_dir,
                "missing_height.txt",
                pd.DataFrame(
                    {
                        "Plot": ["A1"],
                        "Year": [2020],
                        "Species": ["SP1"],
                        "Tree Number": [1],
                        "DBH": [10.0],
                    }
                ),
            )

            imported = convert_text_file_into_dataframe(str(txt_path))
            lowered = convert_columns_to_lowercase(imported)

            with self.assertRaises(ValueError):
                do_mandatory_columns_exist(lowered)

    def test_state_invalid_numeric_and_range_rows_reported(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            txt_path = self._write_tab_file(
                tmp_dir,
                "invalid_values.txt",
                pd.DataFrame(
                    {
                        "Plot": ["A1", "A2", "A3"],
                        "Year": [2020, 2021, 2022],
                        "Species": ["SP1", "SP2", "SP3"],
                        "Tree Number": [1, 2, 3],
                        "DBH": ["bad", 120.0, 10.0],
                        "Height": [12.0, 10.0, 0.8],
                    }
                ),
            )

            imported = convert_text_file_into_dataframe(str(txt_path))
            lowered = convert_columns_to_lowercase(imported)

            self.assertTrue(do_mandatory_columns_exist(lowered))
            errors = validate_tree_dbh_and_height_values(lowered)

            self.assertEqual(len(errors), 3)
            self.assertTrue(any(err["conversion_errors"] for err in errors))
            self.assertTrue(any(err["range_errors"] for err in errors))

    def test_state_missing_dbh_or_height_returns_empty_validation_list(self):
        df = pd.DataFrame(
            {
                "plot": ["A1"],
                "year": [2020],
                "species": ["SP1"],
                "tree number": [1],
                "dbh": [10.0],
            }
        )

        errors = validate_tree_dbh_and_height_values(df)
        self.assertEqual(errors, [])

    def test_state_bad_input_file_returns_none(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            missing_file = Path(tmp_dir) / "does_not_exist.txt"
            imported = convert_text_file_into_dataframe(str(missing_file))
            self.assertIsNone(imported)


class TestDatabaseControllerIntegration(unittest.TestCase):
    def _import_select_data_controller_module(self):
        with redirect_stdout(io.StringIO()):
            return importlib.import_module("controller.Select_Data_Controller")

    @patch("pyodbc.connect")
    def test_import_from_database_success(self, mock_connect):
        sdc_mod = self._import_select_data_controller_module()
        Select_Data_Controller = sdc_mod.Select_Data_Controller

        mock_cursor = MagicMock()
        mock_cursor.description = [
            ("Plot",),
            ("Year",),
            ("Species",),
            ("Tree_number",),
            ("DBH",),
            ("Height",),
        ]
        mock_cursor.fetchall.return_value = [
            ("A1", 2020, 101, 1, decimal.Decimal("10.1"), decimal.Decimal("12.2"))
        ]

        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        dm_instance = MagicMock()
        page = MagicMock()
        view = MagicMock()
        callback = MagicMock()

        controller = Select_Data_Controller.__new__(Select_Data_Controller)
        controller.page = page
        controller.view = view
        controller.data_imported_callback = callback
        controller.is_data_imported = False

        with patch.object(sdc_mod, "DataManager", return_value=dm_instance), patch.object(
            sdc_mod, "Custom_Alert_Dialog"
        ) as mock_alert_cls:
            result = controller.import_from_database(
                db_name="MyDb",
                driver="ODBC Driver 18 for SQL Server",
                server="localhost",
            )

        self.assertTrue(result)
        dm_instance.set_all.assert_called_once()
        saved_rows = dm_instance.set_all.call_args.args[0]
        self.assertEqual(saved_rows[0]["DBH"], 10.1)
        self.assertEqual(saved_rows[0]["Height"], 12.2)
        callback.assert_called_with(True)
        view.update_file_status.assert_called()
        mock_alert_cls.assert_called()

    @patch("pyodbc.connect", side_effect=Exception("42S02"))
    def test_import_from_database_failure_returns_false(self, _mock_connect):
        sdc_mod = self._import_select_data_controller_module()
        Select_Data_Controller = sdc_mod.Select_Data_Controller

        page = MagicMock()
        view = MagicMock()
        callback = MagicMock()

        controller = Select_Data_Controller.__new__(Select_Data_Controller)
        controller.page = page
        controller.view = view
        controller.data_imported_callback = callback
        controller.is_data_imported = False

        with patch.object(sdc_mod, "Display_Error_Dialog") as mock_error_dialog:
            mock_error_dialog.return_value.show.return_value = MagicMock()
            result = controller.import_from_database(
                db_name="MyDb",
                driver="ODBC Driver 18 for SQL Server",
                server="localhost",
            )

        self.assertFalse(result)
        callback.assert_called_with(False)
        view.update_file_status.assert_called_with("Failed to import data from database.")

    @patch("pyodbc.connect")
    def test_import_from_database_uses_selected_db_file_when_args_missing(self, mock_connect):
        sdc_mod = self._import_select_data_controller_module()
        Select_Data_Controller = sdc_mod.Select_Data_Controller

        mock_cursor = MagicMock()
        mock_cursor.description = [
            ("Plot",),
            ("Year",),
            ("Species",),
            ("Tree_number",),
            ("DBH",),
            ("Height",),
        ]
        mock_cursor.fetchall.return_value = [("A1", 2020, 101, 1, decimal.Decimal("10.1"), decimal.Decimal("12.2"))]
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        with tempfile.TemporaryDirectory() as tmp_dir:
            selected_db = os.path.join(tmp_dir, "selected_database.json")
            with open(selected_db, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "server": "localhost",
                        "database": "MyDb",
                        "driver": "ODBC Driver 18 for SQL Server",
                    },
                    f,
                )

            page = MagicMock()
            view = MagicMock()
            callback = MagicMock()
            dm_instance = MagicMock()

            controller = Select_Data_Controller.__new__(Select_Data_Controller)
            controller.page = page
            controller.view = view
            controller.data_imported_callback = callback
            controller.is_data_imported = False

            with patch.object(sdc_mod, "DataManager", return_value=dm_instance), patch.object(
                sdc_mod, "Custom_Alert_Dialog"
            ), patch.object(sdc_mod.json_paths, "SELECTED_DATABASE_PATH", selected_db):
                result = controller.import_from_database()

        self.assertTrue(result)
        mock_connect.assert_called_once()
        callback.assert_called_with(True)

    @patch("pyodbc.connect")
    def test_connect_and_save_db_info_success(self, mock_connect):
        sdc_mod = self._import_select_data_controller_module()
        Select_Data_Controller = sdc_mod.Select_Data_Controller

        mock_conn = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_connect.return_value.__exit__.return_value = False

        page = MagicMock()
        view = MagicMock()
        controller = Select_Data_Controller.__new__(Select_Data_Controller)
        controller.page = page
        controller.view = view
        controller.data_imported_callback = MagicMock()
        controller.is_data_imported = False

        with tempfile.TemporaryDirectory() as tmp_dir:
            selected_db = os.path.join(tmp_dir, "selected_database.json")
            with patch.object(sdc_mod, "get_sql_server_odbc_driver", return_value="ODBC Driver 18 for SQL Server"), patch.object(
                sdc_mod, "get_mssql_data_path", return_value="C:\\SQL\\DATA"
            ), patch.object(sdc_mod.json_paths, "SELECTED_DATABASE_PATH", selected_db):
                ok = controller._connect_and_save_db_info("localhost", "MyDb")

            with open(selected_db, "r", encoding="utf-8") as f:
                saved = json.load(f)

        self.assertTrue(ok)
        self.assertEqual(saved["server"], "localhost")
        self.assertEqual(saved["database"], "MyDb")
        view.add_to_history.assert_called_once_with("localhost", "MyDb")

    @patch("pyodbc.connect", side_effect=Exception("08001"))
    def test_connect_and_save_db_info_failure(self, _mock_connect):
        sdc_mod = self._import_select_data_controller_module()
        Select_Data_Controller = sdc_mod.Select_Data_Controller

        page = MagicMock()
        view = MagicMock()
        controller = Select_Data_Controller.__new__(Select_Data_Controller)
        controller.page = page
        controller.view = view
        controller.data_imported_callback = MagicMock()
        controller.is_data_imported = False

        with patch.object(sdc_mod, "Display_Error_Dialog") as mock_error_dialog:
            mock_error_dialog.return_value.show.return_value = MagicMock()
            ok = controller._connect_and_save_db_info("localhost", "MyDb")

        self.assertFalse(ok)
        page.open.assert_called()

    @patch("pyodbc.connect", side_effect=Exception("28000"))
    def test_connect_and_save_db_info_auth_error_branch(self, _mock_connect):
        sdc_mod = self._import_select_data_controller_module()
        Select_Data_Controller = sdc_mod.Select_Data_Controller

        page = MagicMock()
        view = MagicMock()
        controller = Select_Data_Controller.__new__(Select_Data_Controller)
        controller.page = page
        controller.view = view
        controller.data_imported_callback = MagicMock()
        controller.is_data_imported = False

        with patch.object(sdc_mod, "get_sql_server_odbc_driver", return_value="ODBC Driver 18 for SQL Server"), patch.object(
            sdc_mod, "Display_Error_Dialog"
        ) as mock_error_dialog:
            mock_error_dialog.return_value.show.return_value = MagicMock()
            ok = controller._connect_and_save_db_info("localhost", "MyDb")

        self.assertFalse(ok)
        page.open.assert_called()

    def test_import_from_database_error_code_branches(self):
        sdc_mod = self._import_select_data_controller_module()
        Select_Data_Controller = sdc_mod.Select_Data_Controller

        for err in ["08001", "28000", "Cannot open database 'MyDb' requested by login"]:
            with self.subTest(error=err):
                page = MagicMock()
                view = MagicMock()
                callback = MagicMock()

                controller = Select_Data_Controller.__new__(Select_Data_Controller)
                controller.page = page
                controller.view = view
                controller.data_imported_callback = callback
                controller.is_data_imported = False

                with patch("pyodbc.connect", side_effect=Exception(err)), patch.object(
                    sdc_mod, "Display_Error_Dialog"
                ) as mock_error_dialog:
                    mock_error_dialog.return_value.show.return_value = MagicMock()
                    result = controller.import_from_database(
                        db_name="MyDb",
                        driver="ODBC Driver 18 for SQL Server",
                        server="localhost",
                    )

                self.assertFalse(result)
                page.open.assert_called()
                callback.assert_called_with(False)
                view.update_file_status.assert_called_with("Failed to import data from database.")


class TestAsyncFileImportFlow(unittest.IsolatedAsyncioTestCase):
    def _import_select_data_controller_module(self):
        with redirect_stdout(io.StringIO()):
            return importlib.import_module("controller.Select_Data_Controller")

    class _FakeSpinner:
        def __init__(self, _page):
            self.hidden = False

        def show_dialog(self):
            return None

        async def simulate_progressive_loading(self, *_args, **_kwargs):
            return None

        def hide(self):
            self.hidden = True

    async def test_on_file_selected_cancelled(self):
        sdc_mod = self._import_select_data_controller_module()
        Select_Data_Controller = sdc_mod.Select_Data_Controller

        page = MagicMock()
        page.overlay = []
        view = MagicMock()
        callback = MagicMock()

        controller = Select_Data_Controller.__new__(Select_Data_Controller)
        controller.page = page
        controller.view = view
        controller.selected_file_path = None
        controller.error_messages = []
        controller.data_imported_callback = callback
        controller.is_data_imported = False

        event = types.SimpleNamespace(files=None)

        await controller.on_file_selected(event)

        callback.assert_called_with(False)
        view.update_file_status.assert_called_with("No file selected")
        self.assertFalse(controller.is_data_imported)
        self.assertIsNone(controller.selected_file_path)
        page.update.assert_called()

    async def test_on_file_selected_invalid_dataframe_triggers_error_path(self):
        sdc_mod = self._import_select_data_controller_module()
        Select_Data_Controller = sdc_mod.Select_Data_Controller

        page = MagicMock()
        page.overlay = []
        view = MagicMock()
        callback = MagicMock()

        controller = Select_Data_Controller.__new__(Select_Data_Controller)
        controller.page = page
        controller.view = view
        controller.selected_file_path = None
        controller.error_messages = []
        controller.data_imported_callback = callback
        controller.is_data_imported = False

        event = types.SimpleNamespace(files=[types.SimpleNamespace(path="input.txt")])

        with patch.object(sdc_mod, "Loading_Spinner_Widget", self._FakeSpinner), patch.object(
            sdc_mod, "convert_text_file_into_dataframe", return_value=None
        ), patch.object(sdc_mod, "Display_Error_Dialog") as mock_error_dialog:
            mock_error_dialog.return_value.show.return_value = MagicMock()
            await controller.on_file_selected(event)

        self.assertFalse(controller.is_data_imported)
        callback.assert_called_with(False)
        page.open.assert_called()
        view.update_file_status.assert_called()

    async def test_on_file_selected_success_with_warning_dialog(self):
        sdc_mod = self._import_select_data_controller_module()
        Select_Data_Controller = sdc_mod.Select_Data_Controller

        page = MagicMock()
        page.overlay = []
        view = MagicMock()
        callback = MagicMock()
        dm_instance = MagicMock()

        controller = Select_Data_Controller.__new__(Select_Data_Controller)
        controller.page = page
        controller.view = view
        controller.selected_file_path = None
        controller.error_messages = []
        controller.data_imported_callback = callback
        controller.is_data_imported = False

        df = pd.DataFrame(
            {
                "Plot": ["A1"],
                "Year": [2020],
                "Species": [101],
                "Tree Number": [1],
                "DBH": [10.0],
                "Height": [12.0],
            }
        )
        event = types.SimpleNamespace(files=[types.SimpleNamespace(path="input.txt")])

        with tempfile.TemporaryDirectory() as tmp_dir:
            selected_db_path = os.path.join(tmp_dir, "selected_database.json")
            with patch.object(sdc_mod, "Loading_Spinner_Widget", self._FakeSpinner), patch.object(
                sdc_mod, "convert_text_file_into_dataframe", return_value=df
            ), patch.object(sdc_mod, "do_mandatory_columns_exist", return_value=True), patch.object(
                sdc_mod, "convert_columns_to_specific_types", side_effect=lambda x: x
            ), patch.object(
                sdc_mod, "convert_columns_to_lowercase", side_effect=lambda x: x
            ), patch.object(
                sdc_mod, "check_dataframe_for_nan_values", return_value=(True, 1, [{"index": 0, "nan_columns": ["DBH"]}])
            ), patch.object(
                sdc_mod, "validate_tree_dbh_and_height_values", return_value=[{"index": 0, "range_errors": ["dbh"]}]
            ), patch.object(
                sdc_mod, "DataManager", return_value=dm_instance
            ), patch.object(
                sdc_mod, "Display_Warning_Dialog"
            ) as mock_warning_dialog, patch.object(
                sdc_mod, "Custom_Alert_Dialog"
            ) as mock_alert_dialog, patch.object(
                sdc_mod.json_paths, "SELECTED_DATABASE_PATH", selected_db_path
            ):
                mock_warning_dialog.return_value.show_dialog.return_value = "warning_dialog"
                mock_alert_dialog.return_value.show.return_value = None
                await controller.on_file_selected(event)

        self.assertTrue(controller.is_data_imported)
        callback.assert_called_with(True)
        dm_instance.set_all.assert_called_once()
        self.assertIn("warning_dialog", page.overlay)
        page.update.assert_called()


class TestCalculateBiomassOrchestration(unittest.IsolatedAsyncioTestCase):
    def _import_calculate_controller_module(self):
        with redirect_stdout(io.StringIO()):
            return importlib.import_module("controller.Calculate_Biomass_Controller")

    async def test_calculate_biomass_success_without_missing_species(self):
        calc_mod = self._import_calculate_controller_module()
        Calculate_Biomass_Controller = calc_mod.Calculate_Biomass_Controller

        controller = Calculate_Biomass_Controller.__new__(Calculate_Biomass_Controller)
        controller.view = MagicMock()
        controller.view.get_selected_components.return_value = ["Wood"]
        controller.view.show_species_code_dialog = AsyncMock()
        controller.equation_type = "DBH-based"
        controller.hardwood_and_softwood_species_code_mapping = []

        local_df = pd.DataFrame({"Species": [101], "DBH": [10.0], "Height": [12.0]})
        params_df = pd.DataFrame({"SpeciesCode": [101], "SpecCommon": ["Pine"]})

        with patch.object(calc_mod.pd, "read_json", side_effect=[local_df, params_df]), patch.object(
            calc_mod, "extract_all_the_species_code_from_the_json_files", return_value=[101]
        ), patch.object(
            calc_mod, "extract_all_species_codes_from_local_storage_json", return_value=[101]
        ), patch.object(
            controller, "_lower_column_names"
        ) as mock_lower, patch.object(
            controller, "_process_biomass_calculations"
        ) as mock_process, patch.object(
            controller, "_save_results"
        ) as mock_save:
            ok = await controller.calculate_biomass()

        self.assertTrue(ok)
        controller.view.show_species_code_dialog.assert_not_called()
        mock_lower.assert_called_once()
        mock_process.assert_called_once()
        mock_save.assert_called_once()

    async def test_calculate_biomass_missing_species_dialog_accepted(self):
        calc_mod = self._import_calculate_controller_module()
        Calculate_Biomass_Controller = calc_mod.Calculate_Biomass_Controller

        controller = Calculate_Biomass_Controller.__new__(Calculate_Biomass_Controller)
        controller.view = MagicMock()
        controller.view.get_selected_components.return_value = ["Wood"]
        controller.view.show_species_code_dialog = AsyncMock(return_value={"202": "Hardwood"})
        controller.equation_type = "DBH-based"
        controller.hardwood_and_softwood_species_code_mapping = []

        local_df = pd.DataFrame({"Species": [101, 202], "DBH": [10.0, 11.0], "Height": [12.0, 13.0]})
        params_df = pd.DataFrame({"SpeciesCode": [101], "SpecCommon": ["Pine"]})

        with patch.object(calc_mod.pd, "read_json", side_effect=[local_df, params_df]), patch.object(
            calc_mod, "extract_all_the_species_code_from_the_json_files", return_value=[101]
        ), patch.object(
            calc_mod, "extract_all_species_codes_from_local_storage_json", return_value=[101, 202]
        ), patch.object(
            controller, "_apply_species_type_mapping"
        ) as mock_apply, patch.object(
            controller, "_lower_column_names"
        ), patch.object(
            controller, "_process_biomass_calculations"
        ), patch.object(
            controller, "_save_results"
        ):
            ok = await controller.calculate_biomass()

        self.assertTrue(ok)
        controller.view.show_species_code_dialog.assert_awaited_once()
        mock_apply.assert_called_once()

    async def test_calculate_biomass_missing_species_dialog_cancelled(self):
        calc_mod = self._import_calculate_controller_module()
        Calculate_Biomass_Controller = calc_mod.Calculate_Biomass_Controller

        controller = Calculate_Biomass_Controller.__new__(Calculate_Biomass_Controller)
        controller.view = MagicMock()
        controller.view.get_selected_components.return_value = ["Wood"]
        controller.view.show_species_code_dialog = AsyncMock(return_value=None)
        controller.equation_type = "DBH-based"
        controller.hardwood_and_softwood_species_code_mapping = []

        local_df = pd.DataFrame({"Species": [101, 202], "DBH": [10.0, 11.0], "Height": [12.0, 13.0]})
        params_df = pd.DataFrame({"SpeciesCode": [101], "SpecCommon": ["Pine"]})

        with patch.object(calc_mod.pd, "read_json", side_effect=[local_df, params_df]), patch.object(
            calc_mod, "extract_all_the_species_code_from_the_json_files", return_value=[101]
        ), patch.object(
            calc_mod, "extract_all_species_codes_from_local_storage_json", return_value=[101, 202]
        ), patch.object(
            controller, "_process_biomass_calculations"
        ) as mock_process, patch.object(
            controller, "_save_results"
        ) as mock_save:
            ok = await controller.calculate_biomass()

        self.assertFalse(ok)
        mock_process.assert_not_called()
        mock_save.assert_not_called()


class TestDatabaseWriteIntegration(unittest.TestCase):
    def _import_calculate_controller_module(self):
        with redirect_stdout(io.StringIO()):
            return importlib.import_module("controller.Calculate_Biomass_Controller")

    @patch("pyodbc.connect")
    @patch("builtins.open")
    def test_write_results_to_database_success(self, mock_open_fn, mock_connect):
        calc_mod = self._import_calculate_controller_module()
        Calculate_Biomass_Controller = calc_mod.Calculate_Biomass_Controller

        payload = [
            {
                "Plot": "A1",
                "Year": 2020,
                "Species": 101,
                "Tree Number": 1,
                "DBH": 10.1,
                "Height": 12.2,
                "Wood (KG)": 2.5,
                "Bark (KG)": 1.0,
                "Foliage (KG)": 0.5,
                "Branch (KG)": 0.7,
                "Crown (KG)": 1.2,
                "Stem (KG)": 3.5,
                "Total (KG)": 4.7,
            }
        ]
        mock_open_fn.side_effect = [mock_open(read_data=json.dumps(payload)).return_value]

        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        fake_dm_module = types.ModuleType("data.data_manager")
        dm_instance = MagicMock()
        dm_instance.get_database_path.return_value = "Driver={x};Server=s;Database=d;"
        setattr(fake_dm_module, "DataManager", MagicMock(return_value=dm_instance))

        controller = Calculate_Biomass_Controller.__new__(Calculate_Biomass_Controller)
        controller.equation_type = "DBH-based"

        with patch.dict(sys.modules, {"data.data_manager": fake_dm_module}):
            ok = controller.write_results_to_database()

        self.assertTrue(ok)
        self.assertGreaterEqual(mock_cursor.execute.call_count, 3)
        self.assertTrue(mock_conn.commit.called)

    @patch("pyodbc.connect", side_effect=Exception("db down"))
    def test_write_results_to_database_failure(self, _mock_connect):
        calc_mod = self._import_calculate_controller_module()
        Calculate_Biomass_Controller = calc_mod.Calculate_Biomass_Controller

        fake_dm_module = types.ModuleType("data.data_manager")
        dm_instance = MagicMock()
        dm_instance.get_database_path.return_value = "Driver={x};Server=s;Database=d;"
        setattr(fake_dm_module, "DataManager", MagicMock(return_value=dm_instance))

        controller = Calculate_Biomass_Controller.__new__(Calculate_Biomass_Controller)
        controller.equation_type = "DBH-based"

        with patch.dict(sys.modules, {"data.data_manager": fake_dm_module}):
            ok = controller.write_results_to_database()

        self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main()
