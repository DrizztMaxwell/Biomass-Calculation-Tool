# Main_Controller.py
import flet as ft
from widgets.Component_Card import Component_Card
# Import the Model
from model.Main_Model import Main_Model 
from views.Main_View import Main_View


class Main_Controller:
    """
    Manages event handling and state synchronization between the Model and the View.
    It holds a reference to the Model and the necessary View controls.
    """
    def __init__(self, model: Main_Model, view: Main_View):
        self._model = model
        self.view = view
        # Placeholder for View controls that need *updating*
        self.selected_components_text: ft.Text = None
        self.component_cards_row: ft.Row = None

    def initialize_view_controls(self, selected_components_text: ft.Text, component_cards_row: ft.Row):
        """Called by the View to register the controls the Controller needs to update."""
        self.selected_components_text = selected_components_text
        self.component_cards_row = component_cards_row
        self._refresh_view() # Initial view refresh

    def _create_component_cards(self) -> list[ft.Container]:
        """
        Creates and returns a list of Flet component cards based *only* on the Model state.
        This is the View Factory part of the Controller.
        """
        cards = []
        # Get data from the Model
        for item in self._model.all_component_data:
            # Create the card control, attaching the Controller's handlers
            card = Component_Card(item, on_hover_handler=self.on_hover, on_click_handler=self.on_click)
            cards.append(card)
        return cards

    def build(self):
        return self.view.build()

    def _refresh_view(self):
        """
        Re-renders the dynamic parts of the View. 
        It reads the Model, rebuilds the necessary View controls, and calls update().
        """
        if self.component_cards_row and self.selected_components_text:
            # 1. Re-generate all card controls based on the current Model state
            new_cards = self._create_component_cards()
            self.component_cards_row.controls.clear()
            self.component_cards_row.controls.extend(new_cards)
            
            # 2. Update the selected components text based on the Model
            self.selected_components_text.value = f"Selected: {', '.join(self._model.selected_items)}"
            
            # 3. Call update on the main containers to redraw the View
            self.component_cards_row.update()
            self.selected_components_text.update()
            
    def on_click(self, e: ft.ControlEvent):
        """Handles click on individual component cards (Controller logic)."""
        card_title = e.control.data

        # 1. Update the Model
        self._model.toggle_component(card_title)
            
        # 2. Refresh the View based on the new Model state
        self._refresh_view()