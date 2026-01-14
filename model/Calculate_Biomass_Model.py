#Calculate_Biomass_Model
class Calculate_Biomass_Model:
    def __init__(self):
        self.equation_type = "DBH-based"
        self.selected_components = []
        self.calculation_results = None
        
    def set_equation_type(self, equation_type: str):
        self.equation_type = equation_type
        
    def set_selected_components(self, components: list):
        self.selected_components = components
        
    def get_calculation_results(self):
        return self.calculation_results
        
    def set_calculation_results(self, results):
        self.calculation_results = results