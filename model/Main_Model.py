# Main_Model.py
from data.components_data import COMPONENTS_DATA

class Main_Model:
    """
    Manages the application's state (data model) for component selection.
    It has no knowledge of Flet controls (View).
    """
    def __init__(self):
        # --- Data Model ---
        # Deep copy to ensure the original data source is not mutated globally
        self._components_data = [item.copy() for item in COMPONENTS_DATA]
        self._select_all_data = {
            "title": "Select All",
            "image_src": "./assets/images/list.png",
            "is_selected": False
        }

        # List of currently selected component titles (The core state)
        self.selected_items = [
            item["title"] for item in self._components_data if item.get("is_selected", False)
        ]
        
        # Initial 'Select All' state check
        if len(self.selected_items) == len(self._components_data):
            self._select_all_data["is_selected"] = True

    @property
    def all_component_data(self) -> list[dict]:
        """Returns the combined list of components including 'Select All'."""
        # Ensure the list state is reflected in the select all item before returning
        self._select_all_data["is_selected"] = (len(self.selected_items) == len(self._components_data)) and len(self._components_data) > 0
        return [self._select_all_data] + self._components_data

    def toggle_component(self, title: str):
        """Toggles the selection status of a single component by title."""
        if title == self._select_all_data["title"]:
            self._toggle_select_all()
            return
            
        # 1. Update the component data model
        is_selected = False
        for item in self._components_data:
            if item["title"] == title:
                item["is_selected"] = not item["is_selected"]
                is_selected = item["is_selected"]
                break
        
        # 2. Update the selected_items list
        if is_selected and title not in self.selected_items:
            self.selected_items.append(title)
        elif not is_selected and title in self.selected_items:
            self.selected_items.remove(title)
            
    def _toggle_select_all(self):
        """Toggles the 'Select All' state for all components."""
        
        is_selected = not self._select_all_data["is_selected"]
        self._select_all_data["is_selected"] = is_selected
        
        self.selected_items.clear()
        for item in self._components_data:
            item["is_selected"] = is_selected
            if is_selected:
                self.selected_items.append(item["title"])