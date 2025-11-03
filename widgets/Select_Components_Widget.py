import flet as ft
from data.components_data import COMPONENTS_DATA

def Select_Components_Widget(
    title: ft.Text, 
    description_text: ft.Text,
    components_card_row, 
    selected_card_component,
    components_data=None,
    displayButton=True,
    displayShadow=True,
    on_selection_change=None  # Add callback parameter
):
    # Default components data if none provided
    if components_data is None:
        components_data = COMPONENTS_DATA
    
    # Function to create individual component cards
    def create_component_card(component):
        card = ft.Container(
            width=150,
            height=150,
            border_radius=10,
            bgcolor=ft.Colors.GREEN_50 if component["is_selected"] else ft.Colors.WHITE,
            border=ft.border.all(
                2, 
                ft.Colors.GREEN if component["is_selected"] else ft.Colors.GREY_300
            ),
            padding=10,
            alignment=ft.alignment.center,
            animate_scale=ft.Animation(300, "easeInOut"),
            scale=1.0,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,  # Center vertically
                spacing=8,  # Add consistent spacing between items
                controls=[
                    # Image
                    ft.Container(
                        width=50,
                        height=50,
                        alignment=ft.alignment.center,  # Center the image container
                        content=ft.Image(
                            src=component["image_src"],
                            fit=ft.ImageFit.CONTAIN
                        )
                    ),
                    # Title
                    ft.Container(
                        alignment=ft.alignment.center,  # Center the text container
                        content=ft.Text(
                            value=component["title"],
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLACK,
                            size=18,
                            text_align=ft.TextAlign.CENTER
                        )
                    )
                ]
            ),
            on_click=lambda e, comp=component: toggle_component(e, comp),
            on_hover=lambda e: handle_hover(e, card)
        )
        return card
    
    # Function to handle hover effects
    def handle_hover(e, card):
        if e.data == "true":
            # Mouse enter - scale up
            card.scale = 1.05
        else:
            # Mouse leave - scale back to normal
            card.scale = 1.0
        card.update()
    
    # Function to handle component selection/deselection
    def toggle_component(e, component):
        component["is_selected"] = not component["is_selected"]
        
        # Update the card background color and border
        e.control.bgcolor = ft.Colors.GREEN_50 if component["is_selected"] else ft.Colors.WHITE
        e.control.border = ft.border.all(
            2, 
            ft.Colors.GREEN if component["is_selected"] else ft.Colors.GREY_300
        )
        
        # Update selected components text
        update_selected_text()
        
        # Call the callback if provided
        if on_selection_change:
            selected_items = [comp["title"] for comp in components_data if comp["is_selected"]]
            on_selection_change(selected_items)
        
        e.control.update()
        selected_card_component.update()
    
    # Function to update selected components text
    def update_selected_text():
        selected_items = [comp["title"] for comp in components_data if comp["is_selected"]]
        selected_card_component.value = f"Selected: {', '.join(selected_items)}" if selected_items else "No components selected"
    
    # Function to select all components
    def select_all_components(e):
        all_selected = all(comp["is_selected"] for comp in components_data)
        
        # Toggle all components
        for component in components_data:
            component["is_selected"] = not all_selected
        
        # Update all cards
        for i, component in enumerate(components_data):
            if i < len(components_card_row.controls):
                card = components_card_row.controls[i]
                card.bgcolor = ft.Colors.GREEN_50 if component["is_selected"] else ft.Colors.WHITE
                card.border = ft.border.all(
                    2, 
                    ft.Colors.GREEN if component["is_selected"] else ft.Colors.GREY_300
                )
                card.update()
        
        # Update selected text and button text
        update_selected_text()
        select_all_button.text = "Deselect All" if not all_selected else "Select All"
        
        # Call the callback if provided
        if on_selection_change:
            selected_items = [comp["title"] for comp in components_data if comp["is_selected"]]
            on_selection_change(selected_items)
        
        select_all_button.update()
        selected_card_component.update()
    
    # Clear existing cards and render new ones
    components_card_row.controls.clear()
    for component in components_data:
        card = create_component_card(component)
        components_card_row.controls.append(card)
    
    # Initialize selected components text
    update_selected_text()
    
    # Create Select All button
    select_all_button = ft.TextButton(
        text="Select All",
        icon=ft.Icons.CHECK_BOX_OUTLINED,
        style=ft.ButtonStyle(
            color=ft.Colors.BLUE_500,
        ),
        on_click=select_all_components
    )

    # Create controls list
    controls = [
        title,
        description_text,
        
        # Select All button row
        ft.Row(
            controls=[select_all_button],
            alignment=ft.MainAxisAlignment.START,
        ),
        
        ft.Container(height=10),  # Spacer
        
        components_card_row,

        # Selected Items Display
        ft.Container( 
            expand=True,  # Expand to fill available width
            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.GREEN_ACCENT_400), 
            border_radius=10,
            margin=ft.margin.only(top=10, bottom=10), 
            padding=10, 
            alignment=ft.alignment.center_left,  # Left align the text inside
            content=selected_card_component
        )
    ]

    # Conditionally add Calculate Button
    if displayButton:
        controls.append(
            ft.Row(
                controls=[
                    ft.ElevatedButton(
                        text="Calculate Biomass",
                        icon=ft.Icons.CALCULATE,
                        bgcolor="#28A745",
                        color="#FFFFFF",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=ft.border_radius.all(10)),
                            padding=ft.padding.symmetric(horizontal=20, vertical=10)
                        ),
                        on_click=lambda e: print(f"Calculate button clicked! Selected Components: {[comp['title'] for comp in components_data if comp['is_selected']]}")
                    )
                ],
                alignment=ft.MainAxisAlignment.START,  # Left align the button
            )
        )

    # Conditionally set shadow based on displayShadow parameter
    shadow = None
    if displayShadow:
        shadow = ft.BoxShadow(
            spread_radius=1,
            blur_radius=5,
            color=ft.Colors.with_opacity(0.15, ft.Colors.BLUE_GREY_900),
            offset=ft.Offset(0, 3),
        )

    return ft.Container(
        expand=True,  # Expand to fill parent container
        bgcolor="white",
        padding=20,
        border_radius=10,
        shadow=shadow,  # Use conditional shadow
        alignment=ft.alignment.top_left,  # Align content to top-left
        content=ft.Column(
            controls=controls,
            horizontal_alignment=ft.CrossAxisAlignment.START,  # Left align horizontally
            alignment=ft.MainAxisAlignment.START,  # Align to top
            expand=True,  # Expand to fill the container
        )
    )