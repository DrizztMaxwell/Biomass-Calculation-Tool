import flet as ft

class Create_Species_Model:
    """
    The data model for creating a species, managing the state of selected components.
    """
    def __init__(self, species_code_control :ft.TextField):
        self.species_code_control = species_code_control

    def set_species_code_control(self,value):
        self.species_code_control.value = value

    def get_species_code_control(self):
        return self.species_code_control

    # make this return false

    def is_species_control_valid(self) -> bool:
        """Validates the species code input."""
        value = self.get_species_code_control().value
        # print(f"Validating species code: {value}")
        # Convert to string
        value = str(value)
        #check if alphanumeric, non empty, no whitespace, and length between 3 and 10
        if (value and value.isalnum() and 
            3 <= len(value) <= 10 and 
            ' ' not in value):
            return True
        return False
