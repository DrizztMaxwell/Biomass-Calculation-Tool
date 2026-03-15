import flet as ft
import asyncio


class Loading_Spinner_Widget:
    """
    Reusable loading spinner with progress ring, percentage, and status text.
    Matches app dark/light design language.
    """

    def __init__(
        self,
        page: ft.Page,
        size: int = 72,
        stroke_width: int = 5,
        text_size: int = 16,
        show_loading_text: bool = True,
    ):
        self.page = page
        self.size = size
        self.stroke_width = stroke_width
        self.text_size = text_size
        self.show_loading_text = show_loading_text
        self.progress = 0
        self.is_visible = False
        self._build_widget()

    # ── Theme helpers ─────────────────────────────────────────────────────────

    @property
    def _is_dark(self):
        return self.page.theme_mode == ft.ThemeMode.DARK

    def _bg(self):
        return "#1A1A1A" if self._is_dark else "#FFFFFF"

    def _surface(self):
        return "#222222" if self._is_dark else "#F8FAFC"

    def _border(self):
        return "#2E2E2E" if self._is_dark else "#E2E8F0"

    def _text_primary(self):
        return "#F5F5F5" if self._is_dark else "#0F172A"

    def _text_secondary(self):
        return "#888888" if self._is_dark else "#64748B"

    def _ring_track(self):
        return "#2E2E2E" if self._is_dark else "#E2E8F0"

    # ── Build ─────────────────────────────────────────────────────────────────

    def _build_widget(self):
        # Progress ring
        self.progress_ring = ft.ProgressRing(
            width=self.size,
            height=self.size,
            stroke_width=self.stroke_width,
            color="#16A34A",
            bgcolor=self._ring_track(),
            value=0,
        )

        # Percentage in centre of ring
        self.percentage_text = ft.Text(
            "0%",
            size=self.text_size,
            weight=ft.FontWeight.W_700,
            color=self._text_primary(),
        )

        ring_stack = ft.Stack([
            self.progress_ring,
            ft.Container(
                content=self.percentage_text,
                alignment=ft.alignment.center,
                width=self.size,
                height=self.size,
            ),
        ], width=self.size, height=self.size)

        # Status text
        self.loading_text = ft.Text(
            "Loading...",
            size=13,
            color=self._text_secondary(),
            weight=ft.FontWeight.W_500,
            text_align=ft.TextAlign.CENTER,
        )

        body_controls = [ring_stack]
        if self.show_loading_text:
            body_controls += [
                ft.Container(height=16),
                self.loading_text,
            ]

        # Card
        self.content_card = ft.Container(
            content=ft.Column(
                body_controls,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=0,
                expand=True,
            ),
            padding=ft.padding.symmetric(horizontal=40, vertical=36),
            bgcolor=self._bg(),
            border_radius=ft.border_radius.all(14),
            border=ft.border.all(1, self._border()),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=30,
                color=ft.Colors.with_opacity(0.18, ft.Colors.BLACK),
                offset=ft.Offset(0, 8),
            ),
            width=280,
            height=220,
            alignment=ft.alignment.center,
        )

        self.loading_dialog = ft.AlertDialog(
            modal=True,
            content=self.content_card,
            content_padding=ft.padding.all(0),
            bgcolor=ft.Colors.TRANSPARENT,
            shadow_color=ft.Colors.TRANSPARENT,
            surface_tint_color=ft.Colors.TRANSPARENT,
            inset_padding=ft.padding.all(0),
            shape=ft.RoundedRectangleBorder(radius=14),
            open=False,
        )

        self.container = self.loading_dialog

    def build(self):
        return self.loading_dialog

    # ── Public controls ───────────────────────────────────────────────────────

    def update_progress(self, progress: float):
        self.progress = max(0.0, min(1.0, progress))
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
        if not self.is_visible:
            self.page.dialog = self.loading_dialog
            self.loading_dialog.open = True
            self.is_visible = True
            self.page.update()
        self.page.open(self.loading_dialog)

    def hide(self):
        if self.is_visible:
            self.loading_dialog.open = False
            self.is_visible = False
            self.page.update()

    # ── Async helpers (unchanged logic, kept intact) ──────────────────────────

    async def simulate_progressive_loading(
        self,
        start_progress: float,
        final_progress: float,
        duration: float,
        loading_text: str,
    ):
        self.set_loading_text(loading_text)
        progress_range = final_progress - start_progress
        updates_per_second = 10
        total_updates = max(int(duration * updates_per_second), 1)
        progress_increment = progress_range / total_updates
        current_progress = start_progress
        for _ in range(total_updates):
            current_progress += progress_increment
            current_progress = min(current_progress, final_progress)
            self.update_progress(current_progress)
            await asyncio.sleep(duration / total_updates)
        self.update_progress(final_progress)

    async def simulate_loading(
        self,
        duration: float = 2.0,
        steps: int = 10,
        completion_message: str = "Complete!",
    ):
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