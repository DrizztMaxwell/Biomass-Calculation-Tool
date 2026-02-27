import json
import os
import tempfile
import unittest
from unittest.mock import patch

from controller.Modify_Species_Controller import Modify_Species_Controller


class TestModifySpeciesController(unittest.TestCase):
    def setUp(self):
        self.controller = Modify_Species_Controller()

    def test_get_species_data_defaults_to_empty_list(self):
        self.assertEqual(self.controller.get_species_data(), [])

    def test_set_species_data_updates_internal_state(self):
        payload = [{"SpeciesCode": 101, "SpecCommon": "Pine"}]
        self.controller.set_species_data(payload)
        self.assertEqual(self.controller.get_species_data(), payload)

    def test_load_species_data_reads_existing_json(self):
        payload = [{"SpeciesCode": 202, "SpecCommon": "Spruce"}]

        with tempfile.TemporaryDirectory() as tmp_dir:
            json_path = os.path.join(tmp_dir, "create_species.json")
            with open(json_path, "w", encoding="utf-8") as file_obj:
                json.dump(payload, file_obj)

            with patch("controller.Modify_Species_Controller.json_paths.CREATED_SPECIES_PATH", json_path), patch(
                "controller.Modify_Species_Controller.logger.write"
            ) as mock_logger:
                self.controller.load_species_data()

            self.assertEqual(self.controller.get_species_data(), payload)
            mock_logger.assert_called_once_with("Species data loaded successfully.")

    def test_load_species_data_sets_empty_list_when_file_missing(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            missing_path = os.path.join(tmp_dir, "missing.json")

            with patch("controller.Modify_Species_Controller.json_paths.CREATED_SPECIES_PATH", missing_path), patch(
                "controller.Modify_Species_Controller.logger.write"
            ) as mock_logger:
                self.controller.set_species_data([{"SpeciesCode": 999}])
                self.controller.load_species_data()

            self.assertEqual(self.controller.get_species_data(), [])
            mock_logger.assert_not_called()

    def test_load_species_data_sets_empty_list_when_json_invalid(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            json_path = os.path.join(tmp_dir, "create_species.json")
            with open(json_path, "w", encoding="utf-8") as file_obj:
                file_obj.write("not valid json")

            with patch("controller.Modify_Species_Controller.json_paths.CREATED_SPECIES_PATH", json_path), patch(
                "controller.Modify_Species_Controller.logger.write"
            ) as mock_logger:
                self.controller.set_species_data([{"SpeciesCode": 999}])
                self.controller.load_species_data()

            self.assertEqual(self.controller.get_species_data(), [])
            mock_logger.assert_not_called()

    def test_save_species_data_writes_json_and_returns_true(self):
        payload = [{"SpeciesCode": 303, "SpecCommon": "Fir"}]
        self.controller.set_species_data(payload)

        with tempfile.TemporaryDirectory() as tmp_dir:
            json_path = os.path.join(tmp_dir, "create_species.json")

            with patch("controller.Modify_Species_Controller.json_paths.CREATED_SPECIES_PATH", json_path), patch(
                "controller.Modify_Species_Controller.logger.write"
            ) as mock_logger:
                result = self.controller.save_species_data()

            self.assertTrue(result)
            with open(json_path, "r", encoding="utf-8") as file_obj:
                stored = json.load(file_obj)
            self.assertEqual(stored, payload)
            mock_logger.assert_called_once_with("Species data saved successfully.")

    def test_save_species_data_returns_false_on_write_error(self):
        self.controller.set_species_data([{"SpeciesCode": 404, "SpecCommon": "Maple"}])

        with patch("controller.Modify_Species_Controller.open", side_effect=OSError("disk full")), patch(
            "controller.Modify_Species_Controller.logger.write"
        ) as mock_logger:
            result = self.controller.save_species_data()

        self.assertFalse(result)
        mock_logger.assert_called_once()
        self.assertIn("Error saving data", mock_logger.call_args[0][0])


if __name__ == "__main__":
    unittest.main()
