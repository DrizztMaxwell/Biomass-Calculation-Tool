import flet as ft
import asyncio
import time

class Loading_Spinner_Widget:
    """
    A reusable black loading spinner component with percentage display and built-in loading management.
    Uses AlertDialog for proper modal behavior.
    """
    
    def __init__(self, page: ft.Page, size=64, stroke_width=4, text_size=18, show_loading_text=True):
        self.page = page
        self.size = size
        self.stroke_width = stroke_width
        self.text_size = text_size
        self.progress = 0
        self.is_visible = False
        # Progress Ring and Text setup
        self.progress_ring = ft.ProgressRing(
            width=self.size, height=self.size, stroke_width=self.stroke_width,
            color=ft.Colors.PRIMARY, bgcolor=ft.Colors.GREY_300, value=0
        )
        self.percentage_text = ft.Text(
            "0%", size=self.text_size, weight=ft.FontWeight.BOLD, color=ft.Colors.PRIMARY
        )
        self.loading_stack = ft.Stack(
            [
                self.progress_ring,
                ft.Container(
                    content=self.percentage_text, alignment=ft.alignment.center,
                    width=self.size, height=self.size,
                )
            ],
            width=self.size, height=self.size,
        )
        self.loading_text = ft.Text(
            "Loading...", size=self.text_size - 3 , color=ft.Colors.PRIMARY, weight=ft.FontWeight.BOLD
        )

        controls = [self.loading_stack]
        if show_loading_text:
            # Wrap loading_text in a Container to apply a top margin/padding AND center the text.
            loading_text_container = ft.Container(
                content=self.loading_text, 
                margin=ft.margin.only(top=30),
                alignment=ft.alignment.center 
            )
            controls.append(loading_text_container)

        # Content Card (The white box with spinner) - Adjusted to 400x400
        self.content_card = ft.Container(
            content=ft.Column(
                controls, 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                spacing=0, 
                # Center the column content both ways
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True, 
            ),
            padding=30,
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            border_radius=16,
            shadow=ft.BoxShadow(
                spread_radius=1, blur_radius=20, color=ft.Colors.BLACK26, offset=ft.Offset(0, 4)
            ),
            width=400,  # <-- INCREASED WIDTH
            height=400, # <-- INCREASED HEIGHT
            alignment=ft.alignment.center, 
        )

        # AlertDialog as the main container
        self.loading_dialog = ft.AlertDialog(
            modal=True,
            content=self.content_card,
            content_padding=0,
            bgcolor=ft.Colors.TRANSPARENT,
            shadow_color=ft.Colors.TRANSPARENT,
            inset_padding=0,
            actions_alignment=ft.MainAxisAlignment.CENTER,
            open=False
        )

        # Set the main container for build()
        self.container = self.loading_dialog
    
    def build(self):
        """Return the AlertDialog container."""
        return self.loading_dialog

    def update_progress(self, progress: float):
        self.progress = max(0, min(1, progress))
        self.progress_ring.value = self.progress
        self.percentage_text.value = f"{int(self.progress * 100)}%"
        if self.is_visible:
            self.page.update()
    
    def set_loading_text(self, text: str):
        self.loading_text.value = text
        if self.is_visible:
            self.page.update()
    
    def reset(self):
        self.update_progress(0)
        self.set_loading_text("Loading...")

    def show_dialog(self):
        """Show the loading dialog."""
        if not self.is_visible:
            self.page.dialog = self.loading_dialog
            self.loading_dialog.open = True
            self.is_visible = True
            self.page.update()
        self.page.open(self.loading_dialog)

    def hide(self):
        """Hide the loading dialog."""
        if self.is_visible:
            self.loading_dialog.open = False
            self.is_visible = False
            self.page.update()
        
    async def simulate_progressive_loading(self, start_progress: float, final_progress: float, duration: float, loading_text: str):
        self.set_loading_text(loading_text)

        progress_range = final_progress - start_progress
        updates_per_second = 10
        total_updates = max(int(duration * updates_per_second), 1)  # <- prevent zero division

        progress_increment = progress_range / total_updates
        current_progress = start_progress

        for _ in range(total_updates):
            current_progress += progress_increment
            current_progress = min(current_progress, final_progress)
            self.update_progress(current_progress)
            await asyncio.sleep(duration / total_updates)  # smoother timing

        self.update_progress(final_progress)

        
    async def simulate_loading(self, duration: float = 2.0, steps: int = 10, completion_message: str = "Complete!"):
        self.show_dialog()
        self.reset()
        step_duration = duration / steps
        for i in range(steps + 1):
            progress = i / steps
            self.update_progress(progress)
            self.set_loading_text(f"Processing... {int(progress * 100)}%")
            await asyncio.sleep(step_duration)
        self.set_loading_text(completion_message)
        await asyncio.sleep(0.5)
        self.hide()
    
    def start_loading_with_steps(self, steps_data: list, total_duration: float = None):
        async def run_steps():
            self.show_dialog()
            self.reset()
            for progress, message, step_duration in steps_data:
                self.update_progress(progress)
                self.set_loading_text(message)
                await asyncio.sleep(step_duration)
            self.update_progress(1.0)
            self.set_loading_text("Complete!")
            await asyncio.sleep(0.5)
            self.hide()
        asyncio.create_task(run_steps())
    
    def show_loading_with_callback(self, callback: callable, *args, **kwargs):
        async def execute_with_loading():
            self.show_dialog()
            self.reset()
            try:
                if asyncio.iscoroutinefunction(callback):
                    result = await callback(*args, **kwargs)
                else:
                    result = callback(*args, **kwargs)
                self.update_progress(1.0)
                self.set_loading_text("Complete!")
                await asyncio.sleep(0.5)
                return result
            except Exception as e:
                self.set_loading_text(f"Error: {str(e)}")
                await asyncio.sleep(1.0)
                raise e
            finally:
                self.hide()
        return asyncio.create_task(execute_with_loading())