import os
import flet as ft

from widgets.Equation_Card_Description_Text import Equation_Card_Description_Text
from widgets.Equation_Card_Formula_Text import Equation_Card_Formula_Text
from widgets.Equation_Card_Title_Text import Equation_Card_Title_Text
from widgets.TitleTextWidget import TitleTextWidget
from widgets.DescriptionText import DescriptionText
from widgets.Select_Components_Widget import Select_Components_Widget
from widgets.Equation_Type_Card import Equation_Type_Card
from data.components_data import COMPONENTS_DATA
from widgets.Calculate_Biomass_Button import Calculate_Biomass_Button
#pandas import for dataframe manipulation
import pandas as pd
# Import the Model and Controller
from model.Main_Model import Main_Model 

class Main_View:
    def __init__(self):
        self.selected_components_text = ft.Text(
            value="",
            color=ft.Colors.BLACK,
            weight=ft.FontWeight.W_500
        )
        self.equation_type = "DBH-based"  # Default equation type
        self.component_cards_row = ft.Row(wrap=True)

    def _create_equation_card(self, title: str, formula: str, description: str, radio_value: str) -> Equation_Type_Card:
        """Helper method to create equation type cards."""
        title_formula = ft.Column(
            controls=[
                Equation_Card_Title_Text(title),
                Equation_Card_Formula_Text(formula)
            ],
            spacing=2,
        )
        desc = Equation_Card_Description_Text(description)
       
        return Equation_Type_Card(title_formula, desc, radio_value)
    
    def on_equation_type_change(self, e):
        self.equation_type = e.control.value
        print(f"Selected Equation Type: {self.equation_type}")

    def _create_equation_section(self) -> ft.Container:
        """Create the equation type selection section."""
        equation_cards = [
            self._create_equation_card(
                title="DBH-based",
                formula="B = b₁ × DBHᵇ²",
                description="Uses only Diameter at Breast Height for calculation",
                radio_value="DBH-based"
            ),
            self._create_equation_card(
                title="DBH + Height-based Equation",
                formula="B = b₁ × DBHᵇ² × Heightᵇ³",
                description="Uses both DBH and tree height for more accurate estimation",
                radio_value="DBH + Height-based"
            )
        ]

        radio_group = ft.RadioGroup(
            content=ft.Column(equation_cards),
            on_change=self.on_equation_type_change,
            value="DBH-based"
        )
       
        return ft.Container(
            bgcolor="white",
            padding=20,
            margin=30,
            border_radius=10,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=5,
                color=ft.Colors.with_opacity(0.15, ft.Colors.BLUE_GREY_900),
                offset=ft.Offset(0, 3),
            ),
            content=ft.Column([
                ft.Container(
                    margin=ft.margin.only(top=15, left=5, right=5, bottom=5),
                    content=ft.Column([
                        TitleTextWidget("Equation Type"),
                        DescriptionText("Choose the calculation method for biomass estimation"),
                    ]),
                ),
                radio_group
            ])
        )

    def _create_components_section(self) -> Select_Components_Widget:
        """Create the components selection section."""
        
        return Select_Components_Widget(
            title=TitleTextWidget("Select Tree Component"),
            description_text=DescriptionText("Select tree components for biomass calculation"),
            components_card_row=self.component_cards_row,
            selected_card_component=self.selected_components_text,
            components_data=COMPONENTS_DATA  # Pass the data
            
        )
        
    def on_calculate_biomass_click(self):
        print("Calculate Biomass button clicked.")
        print(f"Equation Type: {self.equation_type}")
        # store selected components in a variable
        selected_components = [comp['title'] for comp in COMPONENTS_DATA if comp['is_selected']]
        print(f"Selected Components: {selected_components}")

        #load the json data from storage/localstorage.json and convert to dataframe
    
        try:
            local_storage_json = pd.read_json("storage/localstorage.json")
            print("Dataframe loaded from localstorage.json:")
            # now load treeparameters.json and for each row in df, lookup the species code in treeparameters.json and print the parameters
            df_tree_params = pd.read_json("data/treeparameters.json")
            print("Tree parameters loaded from treeparameters.json:")
            #column names in json make it lowercase for easier lookup temporarily
            
            df_tree_params.columns = [col.lower() for col in df_tree_params.columns]
            local_storage_json.columns = [col.lower() for col in local_storage_json.columns]

            # now do the lookup and if found then based on components selected and equation type, calculate biomass
            for index, row in local_storage_json.iterrows():
                spec_code = row.get('SpecCode', None)
                if spec_code:
                    #Lookup through json and detect
                    lookup_value_found_in_tree_parameters_json = self._perform_tree_parameters_json_lookup(df_tree_params, spec_code)
                    if lookup_value_found_in_tree_parameters_json:
                        if self.equation_type == "DBH-based":
                           
                           
                            if "Wood" in selected_components:
                                # Wood only
                                
                                bwood1 = lookup_value_found_in_tree_parameters_json.get('bwood1', 0)
                                bwood2 = lookup_value_found_in_tree_parameters_json.get('bwood2', 0)
                                
                                dbh = row.get('DBH', 0)
                                print(f"Calculating Wood Biomass for Row {index} with DBH: {dbh}")
                                if dbh != 0:
                                    biomass = bwood1 * (dbh ** bwood2)
                                    # print(f"Row {index} - Species Code: {spec_code}, Calculated Biomass: {biomass}")
                                    # depending on the components selected add a column to df
                                    local_storage_json.at[index, f'Wood (KG)'] = float(round(biomass, 4))
                                    
                                
                                    #output to file
                                    # local_storage_json.to_json("storage/biomass_results.json", orient='records')
                                    print("Biomass results saved to biomass_results.json")

                            if "Bark" in selected_components:
                                # Bark only
                                bbark1 = lookup_value_found_in_tree_parameters_json.get('bbark1', 0)
                                bbark2 = lookup_value_found_in_tree_parameters_json.get('bbark2', 0)
                                dbh = row.get('DBH', 0)
                                if (dbh != 0):
                                    biomass = bbark1 * (dbh ** bbark2)
                                    # print(f"Row {index} - Species Code: {spec_code}, Calculated Biomass: {biomass}")
                                    # depending on the components selected add a column to df
                                    # local_storage_json.at[index, f'Bark (KG)'] = str(round(biomass, 4))# make into float with 4 decimal places
                                    local_storage_json.at[index, f'Bark (KG)'] = float(round(biomass, 4))

                                    #output to file
                                    # local_storage_json.to_json("storage/biomass_results.json", orient='records')
                                    print("Biomass BARJresults saved to biomass_results.json")
                            if "Foliage" in selected_components:
                                # Foliage only
                                bfoliage1 = lookup_value_found_in_tree_parameters_json.get('bfoliage1', 0)
                                bfoliage2 = lookup_value_found_in_tree_parameters_json.get('bfoliage2', 0)
                                dbh = row.get('DBH', 0)
                                if (dbh != 0):
                                    biomass = bfoliage1 * (dbh ** bfoliage2)
                                    local_storage_json.at[index, f'Foliage (KG)'] = float(round(biomass, 4))
                                    
                                
                                    #output to file
                                    # local_storage_json.to_json("storage/biomass_results.json", orient='records')
                                    print("Biomass results saved to biomass_results.json")
                        
                            if "Branch" in selected_components:
                                # Branch only
                                bbranch1 = lookup_value_found_in_tree_parameters_json.get('bbranches1', 0)
                                bbranch2 = lookup_value_found_in_tree_parameters_json.get('bbranches2', 0)
                                dbh = row.get('DBH', 0)
                                if (dbh != 0):
                                    biomass = bbranch1 * (dbh ** bbranch2)
                                    local_storage_json.at[index, f'Branch (KG)'] = float(round(biomass, 4))
                                    
                                
                                    #output to file
                                    # local_storage_json.to_json("storage/biomass_results.json", orient='records')
                                    print("Biomass results saved to biomass_results.json")
                            
                            if "Crown" in selected_components:
                                #look into value in biomass_results.json if foliage and branch exist then sum them up
                                biomass = 0
                                if "Foliage" in selected_components:
                                    foliage_biomass = local_storage_json.at[index, f'Foliage (KG)']
                                    if pd.notna(foliage_biomass):
                                        biomass += float(foliage_biomass)
                                if "Branch" in selected_components:
                                    branch_biomass = local_storage_json.at[index, f'Branch (KG)']
                                    if pd.notna(branch_biomass):
                                        biomass += float(branch_biomass)
                                
                                        
                                        local_storage_json.at[index, f'Crown (KG)'] = float(round(biomass, 4))
                                        
                                        #output to file
                                        # local_storage_json.to_json("storage/biomass_results.json", orient='records')
                                        print("Biomass results saved to biomass_results.json")
                                            
                            if "Stem" in selected_components:
                                #look into value in biomass_results.json if wood and bark exist then sum them up
                                total_biomass = 0.0
                                dbh = row.get('DBH', 0)
                            
                                bwood1 = lookup_value_found_in_tree_parameters_json.get('bwood1', 0)
                                bwood2 = lookup_value_found_in_tree_parameters_json.get('bwood2', 0)
                                if dbh != 0 and bwood1 != 0 and bwood2 != 0:
                                    wood_biomass = bwood1 * (dbh ** bwood2)
                                    total_biomass += wood_biomass

                                bbark1 = lookup_value_found_in_tree_parameters_json.get('bbark1', 0)
                                bbark2 = lookup_value_found_in_tree_parameters_json.get('bbark2', 0)
                                if dbh != 0 and bbark1 != 0 and bbark2 != 0:
                                    bark_biomass = bbark1 * (dbh ** bbark2)
                                    total_biomass += bark_biomass

                                local_storage_json.at[index, f'Stem (KG)'] = float(round(total_biomass, 4))

                                #output to file
                                # local_storage_json.to_json("storage/biomass_results.json", orient='records')
                                print("Biomass results saved to biomass_results.json")
                            if "Total" in selected_components:
                                    # Sum all biomass components
                                    total_biomass = 0.0
                                    dbh = row.get('DBH', 0)
                                
                                    bwood1 = lookup_value_found_in_tree_parameters_json.get('bwood1', 0)
                                    bwood2 = lookup_value_found_in_tree_parameters_json.get('bwood2', 0)
                                    if dbh != 0 and bwood1 != 0 and bwood2 != 0:
                                        wood_biomass = bwood1 * (dbh ** bwood2)
                                        total_biomass += wood_biomass
                                        # local_storage_json.at[index, f'Wood (KG)'] = str(round(wood_biomass, 4))
                                
                                # Calculate Bark biomass  
                                    bbark1 = lookup_value_found_in_tree_parameters_json.get('bbark1', 0)
                                    bbark2 = lookup_value_found_in_tree_parameters_json.get('bbark2', 0)
                                    if dbh != 0 and bbark1 != 0 and bbark2 != 0:
                                        bark_biomass = bbark1 * (dbh ** bbark2)
                                        total_biomass += bark_biomass
                                        # local_storage_json.at[index, f'Bark (KG)'] = str(round(bark_biomass, 4))
                                
                                # Calculate Foliage biomass
                                    bfoliage1 = lookup_value_found_in_tree_parameters_json.get('bfoliage1', 0)
                                    bfoliage2 = lookup_value_found_in_tree_parameters_json.get('bfoliage2', 0)
                                    if dbh != 0 and bfoliage1 != 0 and bfoliage2 != 0:
                                        foliage_biomass = bfoliage1 * (dbh ** bfoliage2)
                                        total_biomass += foliage_biomass
                                        # local_storage_json.at[index, f'Foliage (KG)'] = str(round(foliage_biomass, 4))
                                
                                # Calculate Branch biomass
                                    bbranch1 = lookup_value_found_in_tree_parameters_json.get('bbranches1', 0)
                                    bbranch2 = lookup_value_found_in_tree_parameters_json.get('bbranches2', 0)
                                    if dbh != 0 and bbranch1 != 0 and bbranch2 != 0:
                                        branch_biomass = bbranch1 * (dbh ** bbranch2)
                                        total_biomass += branch_biomass
                                        # local_storage_json.at[index, f'Branch (KG)'] = str(round(branch_biomass, 4))
                                
                                    # Store the total biomass
                                    local_storage_json.at[index, f'Total (KG)'] = float(round(total_biomass, 4))
                                    
                                    # Output to file
            local_storage_json.to_json("storage/biomass_results.json", orient='records')
            print("Biomass results saved to biomass_results.json")
            #output in a text file the total biomass calculated
            import json

            # Load the data from the JSON file
            with open('storage/biomass_results.json', 'r') as f:
                data = json.load(f)

            # Output in a text file the total biomass calculated
            with open('storage/output.txt', 'w') as f:
                if data:  # Check if data is not empty
                    # Write header
                    headers = list(data[0].keys())
                    f.write('\t'.join(headers) + '\n')
                    
                    # Write data rows
                    for item in data:
                        row = []
                        for header in headers:
                            value = item.get(header, '')
                            # Convert None to empty string and ensure all values are strings
                            if value is None:
                                value = ''
                            row.append(str(value))
                        f.write('\t'.join(row) + '\n')

                print("Data successfully written to output.txt")
                            
  
            
        except Exception as e:
            print(f"Error loading dataframe: {e}")
            return

    def _perform_tree_parameters_json_lookup(self, df_tree_params, spec_code):
        for index,row in df_tree_params.iterrows():
            if row['SpeciesCode'] == spec_code:
                # print(f"Row {index} - Species Code: {spec_code}, Parameters: {row.to_dict()}")
                return row.to_dict()

        #for each row in dataframe, lookup the species code in treeparameters.json and print the parameters
        # with open('data/treeparameters.json', 'r') as f:
            #     tree_params = json.load(f)
            #     for index, row in df.iterrows():
            #         spec_code = row.get('SpecCode', None)
            #         if spec_code:
            #             params = next((item for item in tree_params if item["SpeciesCode"] == spec_code), None)
            #             if params:
            #                 print(f"Row {index} - Species Code: {spec_code}, Parameters: {params}")
            #             else:
            #                 print(f"Row {index} - Species Code: {spec_code} not found in tree parameters.")
            #         else:
            #             print(f"Row {index} - No Species Code provided.")
        
    def build(self) -> ft.Column:
        """Build the main view layout."""
        return ft.Column(
            controls=[
                self._create_equation_section(),
                self._create_components_section(),
                Calculate_Biomass_Button(
                    on_click_callback=self.on_calculate_biomass_click
                ).create()
            ],
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )