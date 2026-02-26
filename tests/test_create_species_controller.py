import unittest
from types import SimpleNamespace
from unittest.mock import patch

from controller.Create_Species_Controller import Create_Species_Controller


class _FakeColumn:
    def __init__(self, values):
        self.values = values
        self.str = SimpleNamespace(lower=lambda: _FakeColumn([str(v).lower() for v in values]))


class _FakeDataSet:
    def __init__(self, data):
        self._data = data
        self.columns = list(data.keys())

    def __getitem__(self, key):
        return _FakeColumn(self._data[key])


class TestCreateSpeciesController(unittest.TestCase):
    def setUp(self):
        self.controller = Create_Species_Controller()

    def test_set_species_code_or_name_sets_value(self):
        self.controller.set_species_code_or_name("123")
        self.assertEqual(self.controller.get_species_code_or_name(), "123")

    def test_handle_create_species_button_click_returns_true_when_valid_and_unique(self):
        self.controller.set_species_code_or_name("123")
        with patch.object(self.controller, "_is_form_valid", return_value=True), patch.object(
            self.controller,
            "_does_species_code_exist_within_dataset",
            side_effect=[False, False],
        ):
            self.assertTrue(self.controller.handle_create_species_button_click())

    def test_handle_create_species_button_click_raises_when_form_invalid(self):
        with patch.object(self.controller, "_is_form_valid", return_value=False):
            with self.assertRaises(ValueError):
                self.controller.handle_create_species_button_click()

    def test_does_species_code_exist_within_dataset_checks_numeric_and_name(self):
        with patch("controller.Create_Species_Controller.pd.read_json") as mock_read_json:
            mock_read_json.return_value = _FakeDataSet({"SpeciesCode": [101, 202]})
            self.assertTrue(self.controller._does_species_code_exist_within_dataset("101", "dummy.json"))

            mock_read_json.return_value = _FakeDataSet({"SpecCommon": ["Pine", "Spruce"]})
            self.assertTrue(self.controller._does_species_code_exist_within_dataset("pine", "dummy.json"))

    def test_check_if_species_code_is_an_integer_valid_and_invalid(self):
        self.assertEqual(self.controller._check_if_species_code_is_an_integer("25"), 25)
        with self.assertRaises(ValueError):
            self.controller._check_if_species_code_is_an_integer("-1")

    def test_validate_species_code_or_name_value_numeric_and_alpha(self):
        self.assertEqual(self.controller._validate_species_code_or_name_value("42"), 42)
        self.assertEqual(self.controller._validate_species_code_or_name_value("Pine"), "Pine")

    def test_is_form_valid_true_when_all_sections_valid(self):
        self.controller.set_species_code_or_name("10")
        self.controller.set_selected_components(["Wood"])
        self.controller.set_origin_type("Natural Stand")
        self.controller.set_current_equation_type("DBH-based")
        self.controller.set_param_controls(
            {
                "DBH-based": {
                    "Wood": [SimpleNamespace(visible=True, value="1.2", label="b1")],
                }
            }
        )

        self.assertTrue(self.controller._is_form_valid())

    def test_is_form_valid_raises_when_no_component_selected(self):
        self.controller.set_species_code_or_name("10")
        self.controller.set_selected_components([])
        self.controller.set_origin_type("Natural Stand")
        self.controller.set_current_equation_type("DBH-based")

        with self.assertRaises(ValueError):
            self.controller._is_form_valid()

    def test_validate_parameter_values_rejects_text_and_out_of_range(self):
        self.controller.set_selected_components(["Wood"])
        self.controller.set_current_equation_type("DBH-based")

        self.controller.set_param_controls(
            {
                "DBH-based": {
                    "Wood": [SimpleNamespace(visible=True, value="abc", label="b1")],
                }
            }
        )
        with self.assertRaises(ValueError):
            self.controller.validate_parameter_values()

        self.controller.set_param_controls(
            {
                "DBH-based": {
                    "Wood": [SimpleNamespace(visible=True, value="6.0", label="b1")],
                }
            }
        )
        with self.assertRaises(ValueError):
            self.controller.validate_parameter_values()


if __name__ == "__main__":
    unittest.main()
