#Calculate_Biomass_Controller
from ast import Dict, List
import json
import os
from datetime import datetime
import flet as ft
import pandas as pd
import pyodbc
from widgets.LogFileTxt import logger
from widgets.Bar_Chart_Widget import Bar_Chart_Widget
from constants.Biomass_Config import Biomass_Config
from helper_functions.Biomass_Calculator.did_user_import_from_database import did_user_import_from_database
from helper_functions.Biomass_Calculator.export_to_text_file import export_to_text_file
from helper_functions.Biomass_Calculator.convert_json_to_dataframe import convert_json_to_dataframe
from helper_functions.Biomass_Calculator.reorder_by_species_code import reorder_by_species_code
from helper_functions.Biomass_Calculator.extract_all_species_code_from_local_storage_json import extract_all_species_codes_from_local_storage_json
from helper_functions.Biomass_Calculator.extract_all_the_species_code_from_the_json_files import extract_all_the_species_code_from_the_json_files
from constants.Json_File_Path_Constants import json_paths

# ── Created-species key normaliser ───────────────────────────────────────────
_DBH_KEY_MAP = {
    "bwoodb1":     "bwood1",     "bwoodb2":     "bwood2",
    "bbarkb1":     "bbark1",     "bbarkb2":     "bbark2",
    "bbranchesb1": "bbranches1", "bbranchesb2": "bbranches2",
    "bfoliageb1":  "bfoliage1",  "bfoliageb2":  "bfoliage2",
}
_DBH_H_KEY_MAP = {
    "bhwoodb1":     "bhwood1",     "bhwoodb2":     "bhwood2",    "bhwoodb3":     "bhwood3",
    "bhbarkb1":     "bhbark1",     "bhbarkb2":     "bhbark2",    "bhbarkb3":     "bhbark3",
    "bhbranchesb1": "bhbranches1", "bhbranchesb2": "bhbranches2","bhbranchesb3": "bhbranches3",
    "bhfoliageb1":  "bhfoliage1",  "bhfoliageb2":  "bhfoliage2", "bhfoliageb3":  "bhfoliage3",
}

# ── Table name resolver ───────────────────────────────────────────────────────
# DBH-based           → dbo.tCalcBiomassOutputD
# DBH + Height-based  → dbo.tCalcBiomassOutputDH
_TABLE_NAME_MAP = {
    "DBH-based":          "tCalcBiomassOutputD",
    "DBH + Height-based": "tCalcBiomassOutputDH",
}

def _resolve_table_name(equation_type: str) -> str:
    """Return the correct output table name for the given equation type."""
    table = _TABLE_NAME_MAP.get(equation_type)
    if table is None:
        raise ValueError(
            f"Unknown equation type '{equation_type}'. "
            f"Expected one of: {list(_TABLE_NAME_MAP.keys())}"
        )
    return table

# ─────────────────────────────────────────────────────────────────────────────

def _normalise_created_species_params(species: dict) -> dict:
    """
    Remap created_species.json keys (bwoodb1, bbarkb2 etc.)
    to tree_params format (bwood1, bbark2 etc.).
    """
    equation_type = species.get("EquationType", "DBH-based")
    key_map       = _DBH_H_KEY_MAP if "Height" in equation_type else _DBH_KEY_MAP
    normalised    = dict(species)
    for src_key, target_key in key_map.items():
        v = species.get(src_key)
        if v is not None:
            normalised[target_key] = float(v)
    return normalised

# ─────────────────────────────────────────────────────────────────────────────


class Calculate_Biomass_Controller:
    """Controller for calculating tree biomass based on selected components and equation types."""

    def __init__(self, view):
        self.view = view
        self.equation_type = "DBH-based"
        self.local_storage_data = pd.read_json(json_paths.LOCAL_STORAGE_PATH)
        self.tree_params_data = pd.read_json(json_paths.TREE_PARAMS_PATH)
        self.selected_components = []
        self.is_database_selected = False
        self.hardwood_and_softwood_species_code_mapping = []
        self.is_database_selected = did_user_import_from_database()

    def get_database_selected_flag(self) -> bool:
        return self.is_database_selected

    async def _on_write_database_click(self, event):
        from widgets.Loading_Spinner_Widget import Loading_Spinner_Widget
        print("Write to database button clicked")
        loading_spinner = Loading_Spinner_Widget(self.view.page)
        loading_spinner.show_dialog()
        await loading_spinner.simulate_progressive_loading(0.0, 0.5, 0.1, "Writing to database...")
        success = self.write_results_to_database()
        logger.write(f"Write to database operation success: {success}")
        await loading_spinner.simulate_progressive_loading(1.0, 1.0, 0.1, "Completed...")
        loading_spinner.hide()
        if not success:
            self.view.show_error_dialog(title="Error", message="Failed to write results to database.")
            return
        table_name = _resolve_table_name(self.get_equation_type())
        self.view.show_success_dialog(
            title="Success",
            message=f"Successfully exported data to dbo.{table_name}."
        )

    def export_results_to_text_file(self, file_path: str) -> bool:
        if export_to_text_file(file_path):
            self.view.show_success_dialog(title="Export Successful", message=f"Data exported successfully to {file_path}")
            return True
        self.view.show_error_dialog(title="Export Failed", message=f"Failed to export data to {file_path}")
        return False

    async def on_calculate_biomass_click(self, event):
        from widgets.Loading_Spinner_Widget import Loading_Spinner_Widget
        logger.write("Calculate biomass button clicked")
        loading_spinner = Loading_Spinner_Widget(self.view.page)
        loading_spinner.show_dialog()
        self.view.disable_calculation_button(event.control)
        await loading_spinner.simulate_progressive_loading(0.0, 0.2, 0.1, "Beginning Calculation...")
        calculation_success = await self.calculate_biomass()
        if not calculation_success:
            self.view.enable_calculation_button(event.control)
            loading_spinner.hide()
            return
        await loading_spinner.simulate_progressive_loading(1.0, 1.0, 0.1, "Completed...")
        loading_spinner.hide()
        self.view.show_results()
        self.view.enable_calculation_button(event.control)

    def _get_sum_of_component_for_specific_species(self, data: pd.DataFrame, species_code: int, component: str) -> float:
        filtered_data = data[data['species'].astype(str) == str(species_code)]
        component_column = f"{component} (KG)"
        if component_column in filtered_data.columns:
            return filtered_data[component_column].sum()
        return 0.0

    def _click_on_show_chart_button(self) -> list:
        species_data_for_chart = []
        data = convert_json_to_dataframe(Biomass_Config.BIOMASS_RESULTS_PATH)
        data = reorder_by_species_code(data)
        species_codes = self._extract_all_species_codes(data)
        for species_code in species_codes:
            wood_sum    = self._get_sum_of_component_for_specific_species(data, species_code, "Wood")
            bark_sum    = self._get_sum_of_component_for_specific_species(data, species_code, "Bark")
            branch_sum  = self._get_sum_of_component_for_specific_species(data, species_code, "Branch")
            foliage_sum = self._get_sum_of_component_for_specific_species(data, species_code, "Foliage")
            if wood_sum == 0 and bark_sum == 0 and branch_sum == 0 and foliage_sum == 0:
                continue
            species_data_for_chart.append({
                "species_code": species_code,
                "Wood":    wood_sum,
                "Bark":    bark_sum,
                "Branch":  branch_sum,
                "Foliage": foliage_sum,
            })
        return species_data_for_chart

    def _extract_all_species_codes(self, data: pd.DataFrame) -> list:
        if 'species' in data.columns:
            return data['species'].unique().tolist()
        return []

    def set_equation_type(self, equation_type: str) -> None:
        self.equation_type = equation_type

    def get_equation_type(self) -> str:
        return self.equation_type

    def build(self):
        return self.view.build()

    def checkbox(self):
        pass

    def check_if_species_code_exists_within_the_json_files(self, species_code: int, json_file_path_1: str, json_file_path_2: str) -> bool:
        try:
            with open(json_file_path_1, 'r') as f1, open(json_file_path_2, 'r') as f2:
                data1 = json.load(f1)
                data2 = json.load(f2)
                species_codes_1 = {int(item['SpeciesCode']) for item in data1 if 'SpeciesCode' in item}
                species_codes_2 = {int(item['SpeciesCode']) for item in data2 if 'SpeciesCode' in item}
                return species_code in species_codes_1 or species_code in species_codes_2
        except Exception as e:
            print(f"Error checking species code existence: {e}")
            return False

    def _create_hardwood_softwood_species_code_mapping(self, hardwood_species_codes: list, softwood_species_codes: list) -> dict:
        mapping = {}
        for code in hardwood_species_codes:
            mapping[code] = "hardwood"
        for code in softwood_species_codes:
            mapping[code] = "softwood"
        return mapping

    def _apply_species_type_mapping(self, species_type_mapping):
        for species_code, wood_type in species_type_mapping.items():
            if wood_type == "Hardwood":
                self._set_hardwood_parameters(species_code)
            elif wood_type == "Softwood":
                self._set_softwood_parameters(species_code)

    def _set_hardwood_parameters(self, species_code):
        hardwood_records = self.tree_params_data.loc[
            self.tree_params_data['SpecCommon'] == 'Hardwood'
        ].to_dict('records')
        if not hardwood_records:
            print("No hardwood records found in tree_params_data")
            return
        for record in hardwood_records:
            record['SpeciesCode'] = species_code
        self.hardwood_and_softwood_species_code_mapping.append(hardwood_records)

    def _set_softwood_parameters(self, species_code):
        softwood_records = self.tree_params_data.loc[
            self.tree_params_data['SpecCommon'] == 'Softwood'
        ].to_dict('records')
        if not softwood_records:
            return
        for record in softwood_records:
            record['SpeciesCode'] = species_code
        self.hardwood_and_softwood_species_code_mapping.append(softwood_records)

    async def calculate_biomass(self) -> bool:
        self.hardwood_and_softwood_species_code_mapping = []
        self.selected_components = self.view.get_selected_components()
        self.equation_type = self.get_equation_type()
        try:
            self.local_storage_data = pd.read_json(Biomass_Config.LOCAL_STORAGE_PATH)
            self.tree_params_data   = pd.read_json(Biomass_Config.TREE_PARAMS_PATH)
            datasets_species_code_list    = extract_all_the_species_code_from_the_json_files(
                Biomass_Config.TREE_PARAMS_PATH, Biomass_Config.CREATED_SPECIES_PATH
            )
            local_storage_species_code_list = extract_all_species_codes_from_local_storage_json(
                self.local_storage_data
            )
            datasets_species_code_list      = [str(c).lower() for c in datasets_species_code_list]
            local_storage_species_code_list = [str(c).lower() for c in local_storage_species_code_list]
            missing_species_codes = set(local_storage_species_code_list) - set(datasets_species_code_list)
            if missing_species_codes:
                species_type_mapping = await self.view.show_species_code_dialog(missing_species_codes)
                if species_type_mapping is None:
                    raise Exception("Dialog cancelled by user")
                self._apply_species_type_mapping(species_type_mapping)
            self._lower_column_names(self.local_storage_data, self.tree_params_data)
            self._process_biomass_calculations(self.local_storage_data, self.tree_params_data)
            self._save_results(self.local_storage_data)
            return True
        except Exception as e:
            print(f"Error calculating biomass: {e}")
            return False

    def _lower_column_names(self, *dataframes) -> None:
        for df in dataframes:
            df.columns = df.columns.str.lower()

    def lookup(self, data, species_code: int) -> dict:
        species_code_lookup = {int(dat["speciescode"]): dat for dat in data}
        return species_code_lookup.get(species_code)

    def _process_biomass_calculations(self, local_data: pd.DataFrame, tree_params: pd.DataFrame) -> None:
        """Calculate biomass for each row — with created_species key normalisation fix."""

        species_code_lookup  = {}
        species_name_lookup  = {}
        created_species_code_lookup = {}
        created_species_name_lookup = {}
        hardwood_and_softwood_species_code_mapping_lookup = {}

        # Build tree_params lookups
        for _, row in tree_params.iterrows():
            code = row['speciescode']
            if code and pd.notna(code):
                species_code_lookup[int(code)] = row.to_dict()
            name = row.get('speccommon')
            if name and pd.notna(name):
                species_name_lookup[str(name).lower().strip()] = row.to_dict()

        # Build created_species lookups
        try:
            with open(json_paths.CREATED_SPECIES_PATH, "r") as f:
                created_species_data = json.load(f)

            for species in created_species_data:
                normalised = _normalise_created_species_params(species)
                code = normalised.get('SpeciesCode')
                name = normalised.get('SpecCommon')

                if code and pd.notna(code):
                    try:
                        created_species_code_lookup[int(code)] = normalised
                    except (ValueError, TypeError):
                        pass

                if name and pd.notna(name):
                    created_species_name_lookup[str(name).lower().strip()] = normalised

        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load created_species.json: {e}")

        # Build hardwood/softwood mapping lookup
        for species_list in self.hardwood_and_softwood_species_code_mapping:
            for species in species_list:
                try:
                    code = species.get('SpeciesCode')
                    if str(code).isdigit():
                        code = int(code)
                    else:
                        code = str(code).lower().strip()
                    if code and pd.notna(code):
                        hardwood_and_softwood_species_code_mapping_lookup[code] = species
                except (ValueError, TypeError):
                    continue

        # Process each row
        for idx, row in local_data.iterrows():
            species_value  = row.get('species')
            species_params = None

            try:
                species_code   = int(species_value)
                species_params = (
                    species_code_lookup.get(species_code) or
                    created_species_code_lookup.get(species_code) or
                    hardwood_and_softwood_species_code_mapping_lookup.get(species_code)
                )
            except (ValueError, TypeError):
                species_name   = str(species_value).lower().strip()
                species_params = (
                    species_name_lookup.get(species_name) or
                    created_species_name_lookup.get(species_name) or
                    hardwood_and_softwood_species_code_mapping_lookup.get(species_name)
                )

            if species_params:
                self._calculate_row_biomass(local_data, idx, row, species_params)

    def _get_species_parameters(self, tree_params: pd.DataFrame, species_code: int) -> dict:
        data_as_dict = tree_params.to_dict('records')
        return self.lookup(data_as_dict, species_code)

    def _calculate_row_biomass(self, data: pd.DataFrame, index: int, row: pd.Series, species_params: dict) -> None:
        if self.equation_type == "DBH-based":
            self._calculate_dbh_based_biomass(data, index, row, species_params)
        if self.equation_type == "DBH + Height-based":
            self._calculate_dbh_height_based_biomass(data, index, row, species_params)

    def _calculate_dbh_height_based_biomass(self, data: pd.DataFrame, index: int, row: pd.Series, species_params: dict) -> None:
        raw_dbh    = row.get('dbh')
        raw_height = row.get('height')
        try:
            dbh    = float(raw_dbh)    if raw_dbh    is not None and str(raw_dbh).strip()    != '' else 0.0
            height = float(raw_height) if raw_height is not None and str(raw_height).strip() != '' else 0.0
        except (ValueError, TypeError):
            return
        if dbh == 0.0 or height == 0.0:
            return

        wood_p1    = float(species_params.get("bhwood1",     0))
        wood_p2    = float(species_params.get("bhwood2",     0))
        wood_p3    = float(species_params.get("bhwood3",     0))
        bark_p1    = float(species_params.get("bhbark1",     0))
        bark_p2    = float(species_params.get("bhbark2",     0))
        bark_p3    = float(species_params.get("bhbark3",     0))
        branch_p1  = float(species_params.get("bhbranches1", 0))
        branch_p2  = float(species_params.get("bhbranches2", 0))
        branch_p3  = float(species_params.get("bhbranches3", 0))
        foliage_p1 = float(species_params.get("bhfoliage1",  0))
        foliage_p2 = float(species_params.get("bhfoliage2",  0))
        foliage_p3 = float(species_params.get("bhfoliage3",  0))

        def bh(b1, b2, b3): return b1 * (dbh ** b2) * (height ** b3)

        if "Wood"    in self.selected_components:
            data.at[index, 'Wood (KG)']    = round(bh(wood_p1,   wood_p2,   wood_p3),   4)
        if "Bark"    in self.selected_components:
            data.at[index, 'Bark (KG)']    = round(bh(bark_p1,   bark_p2,   bark_p3),   4)
        if "Branch"  in self.selected_components:
            data.at[index, 'Branch (KG)']  = round(bh(branch_p1, branch_p2, branch_p3), 4)
        if "Foliage" in self.selected_components:
            data.at[index, 'Foliage (KG)'] = round(bh(foliage_p1,foliage_p2,foliage_p3),4)
        if "Stem"    in self.selected_components:
            data.at[index, 'Stem (KG)']    = round(bh(wood_p1,wood_p2,wood_p3) + bh(bark_p1,bark_p2,bark_p3), 4)
        if "Crown"   in self.selected_components:
            data.at[index, 'Crown (KG)']   = round(bh(foliage_p1,foliage_p2,foliage_p3) + bh(branch_p1,branch_p2,branch_p3), 4)
        
        if "Total"   in self.selected_components:
            data.at[index, 'Total (KG)']   = round(
                bh(wood_p1,wood_p2,wood_p3) + bh(bark_p1,bark_p2,bark_p3) +
                bh(foliage_p1,foliage_p2,foliage_p3) + bh(branch_p1,branch_p2,branch_p3), 4
            )

    def _calculate_dbh_height_based_biomass_for_wood(self, dbh, height, p1, p2, p3):
        return float(p1 * (dbh ** p2) * (height ** p3))
    def _calculate_dbh_height_based_biomass_for_bark(self, dbh, height, p1, p2, p3):
        return float(p1 * (dbh ** p2) * (height ** p3))
    def _calculate_dbh_height_based_biomass_for_branch(self, dbh, height, p1, p2, p3):
        return float(p1 * (dbh ** p2) * (height ** p3))
    def _calculate_dbh_height_based_biomass_for_foliage(self, dbh, height, p1, p2, p3):
        return float(p1 * (dbh ** p2) * (height ** p3))

    def _calculate_dbh_based_biomass(self, data: pd.DataFrame, index: int, row: pd.Series, species_params: dict) -> None:
        raw_dbh = row.get('dbh', 0)
        try:
            dbh = float(raw_dbh) if raw_dbh is not None and str(raw_dbh).strip() != '' else 0.0
        except (ValueError, TypeError):
            return
        if dbh == 0.0:
            return
        self._calculate_individual_components(data, index, species_params, dbh)
        self._calculate_composite_components(data, index, species_params, dbh)

    def _calculate_individual_components(self, data, index, species_params, dbh):
        component_configs = [
            ("Wood",    "wood",     "bwood1",     "bwood2"),
            ("Bark",    "bark",     "bbark1",     "bbark2"),
            ("Foliage", "foliage",  "bfoliage1",  "bfoliage2"),
            ("Branch",  "branches", "bbranches1", "bbranches2"),
        ]
        for display_name, component, param1, param2 in component_configs:
            if display_name in self.selected_components:
                self._calculate_component_biomass(data, index, species_params, dbh, component, param1, param2)

    def _calculate_composite_components(self, data, index, species_params, dbh):
        if "Crown" in self.selected_components:
            self._calculate_crown_biomass(data, index, species_params, dbh)
        if "Stem"  in self.selected_components:
            self._calculate_stem_biomass(data, index, species_params, dbh)
        if "Total" in self.selected_components:
            self._calculate_total_biomass(data, index, species_params, dbh)

    def _calculate_component_biomass(self, data, index, species_params, dbh, component, param1, param2):
        p1 = species_params.get(param1, 0)
        p2 = species_params.get(param2, 0)
        if dbh == 0 and p1 == 0 and p2 == 0:
            return
        biomass     = p1 * (dbh ** p2)
        column_name = "Branch (KG)" if component == "branches" else f"{component.title()} (KG)"
        data.at[index, column_name] = float(round(biomass, 4))

    def _calculate_crown_biomass(self, data, index, species_params, dbh):
        crown = (
            self._calculate_single_component(species_params, dbh, 'bfoliage1',  'bfoliage2') +
            self._calculate_single_component(species_params, dbh, 'bbranches1', 'bbranches2')
        )
        if crown > 0:
            data.at[index, 'Crown (KG)'] = float(round(crown, 4))

    def _calculate_stem_biomass(self, data, index, species_params, dbh):
        stem = (
            self._calculate_single_component(species_params, dbh, 'bwood1', 'bwood2') +
            self._calculate_single_component(species_params, dbh, 'bbark1', 'bbark2')
        )
        if stem > 0:
            data.at[index, 'Stem (KG)'] = float(round(stem, 4))

    def _calculate_total_biomass(self, data, index, species_params, dbh):
        total = sum([
            self._calculate_single_component(species_params, dbh, 'bwood1',     'bwood2'),
            self._calculate_single_component(species_params, dbh, 'bbark1',     'bbark2'),
            self._calculate_single_component(species_params, dbh, 'bfoliage1',  'bfoliage2'),
            self._calculate_single_component(species_params, dbh, 'bbranches1', 'bbranches2'),
        ])
        if total > 0:
            data.at[index, 'Total (KG)'] = float(round(total, 4))

    def _calculate_single_component(self, species_params, dbh, param1, param2) -> float:
        p1 = species_params.get(param1, 0)
        p2 = species_params.get(param2, 0)
        if dbh != 0 and p1 != 0 and p2 != 0:
            return p1 * (dbh ** p2)
        return 0.0

    def _save_results(self, data: pd.DataFrame) -> None:
        data.to_json(json_paths.BIOMASS_RESULTS_PATH, orient='records')
        self._save_to_text_file(data)

    def _save_to_text_file(self, data: pd.DataFrame) -> None:
        try:
            records = data.to_dict('records')
            with open(json_paths.OUTPUT_TEXT_PATH, 'w') as file:
                if records:
                    headers = list(records[0].keys())
                    file.write('\t'.join(headers) + '\n')
                    for record in records:
                        file.write('\t'.join(str(record.get(h, '')) for h in headers) + '\n')
        except Exception as e:
            print(f"Error saving to text file: {e}")

    def _normalize_biomass_row(self, row: dict) -> dict:
        plot        = row.get("Plot")        or row.get("plot")
        year        = row.get("Year")        or row.get("year")
        tree_number = row.get("Tree_number") or row.get("Tree Number") or row.get("tree_number")
        species     = row.get("Species")     or row.get("species")     or row.get("SpecCode")
        if not plot or year is None or tree_number is None or species is None:
            raise ValueError(f"Missing required fields in row: {row}")
        return {
            "plot":               plot,
            "year":               int(year),
            "species":            int(species),
            "tree_number":        int(tree_number),
            "dbh":                row.get("DBH")           or row.get("dbh"),
            "height":             row.get("Height")        or row.get("height"),
            "wood_kg":            row.get("Wood (KG)")     or row.get("wood_kg"),
            "bark_kg":            row.get("Bark (KG)")     or row.get("bark_kg"),
            "branch_kg":          row.get("Branch (KG)")   or row.get("branch_kg"),
            "foliage_kg":         row.get("Foliage (KG)")  or row.get("foliage_kg"),
            "stem_kg":            row.get("Stem (KG)")     or row.get("stem_kg"),
            "crown_kg":           row.get("Crown (KG)")    or row.get("crown_kg"),
            "total_kg":           row.get("Total (KG)")    or row.get("total_kg"),
            "coefficient_source": self.get_equation_type(),
        }

    def write_results_to_database(self):
        try:
            from data.data_manager import DataManager
            dm         = DataManager()
            db_path    = dm.get_database_path()
            conn       = pyodbc.connect(db_path)
            cursor     = conn.cursor()

            # ── Resolve table name from equation type ─────────────────────────
            table_name = _resolve_table_name(self.get_equation_type())
            # e.g. "tCalcBiomassOutputD" or "tCalcBiomassOutputDH"
            # ─────────────────────────────────────────────────────────────────
            # Drop table if it exists, then recreate fresh
            drop_table_sql = f"""
            IF EXISTS (
                SELECT 1 FROM sys.tables t
                JOIN sys.schemas s ON t.schema_id = s.schema_id
                WHERE t.name = '{table_name}' AND s.name = 'dbo'
            )
            DROP TABLE dbo.{table_name};
            """
            cursor.execute(drop_table_sql)
            conn.commit()
 
            create_table_sql = f"""
            IF NOT EXISTS (
                SELECT 1 FROM sys.tables t
                JOIN sys.schemas s ON t.schema_id = s.schema_id
                WHERE t.name = '{table_name}' AND s.name = 'dbo'
            )
            CREATE TABLE dbo.{table_name} (
                Plot              VARCHAR(100)      NOT NULL,
                Year              INT               NOT NULL,
                Species           INT               NOT NULL,
                Tree_number       INT               NOT NULL,
                DBH               DECIMAL(4,1)      NOT NULL,
                Height            DECIMAL(4,2)      NULL,
                Wood_kg           NUMERIC(10,1),
                Bark_kg           NUMERIC(10,1),
                Branch_kg         NUMERIC(10,1),
                Foliage_kg        NUMERIC(10,1),
                Stem_kg           NUMERIC(10,1),
                Crown_kg          NUMERIC(10,1),
                Total_kg          NUMERIC(10,1),
                CoefficientSource VARCHAR(100)      NULL,
                processed_at      DATETIMEOFFSET    NOT NULL DEFAULT SYSUTCDATETIME()
            );
            """
            cursor.execute(create_table_sql)
            conn.commit()

            # Clear only the relevant table before re-inserting
            cursor.execute(f"DELETE FROM dbo.{table_name}")
            conn.commit()

            with open(json_paths.BIOMASS_RESULTS_PATH, 'r') as f:
                data = json.load(f)

            insert_sql = f"""
            INSERT INTO dbo.{table_name}
            (Plot, Year, Species, Tree_number, DBH, Height,
             Wood_kg, Bark_kg, Branch_kg, Foliage_kg, Stem_kg, Crown_kg, Total_kg, CoefficientSource)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.fast_executemany = True
            for row in data:
                r = self._normalize_biomass_row(row)
                cursor.execute(insert_sql,
                    r["plot"], r["year"], r["species"], r["tree_number"],
                    r["dbh"], r["height"],
                    _to_one_decimal(r["wood_kg"]),
                    _to_one_decimal(r["bark_kg"]),
                    _to_one_decimal(r["branch_kg"]),
                    _to_one_decimal(r["foliage_kg"]),
                    _to_one_decimal(r["stem_kg"]),
                    _to_one_decimal(r["crown_kg"]),
                    _to_one_decimal(r["total_kg"]),
                    r.get("coefficient_source"),
                )
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Database write error: {e}")
            return False


def _to_one_decimal(value):
    return round(value, 1) if value is not None else None