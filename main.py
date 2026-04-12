import flet as ft
import asyncio
from data.data_manager import DataManager
from views.EULA.EULA_View import EULA_View
from views.SideNavbar_View import SideNavbar_View
from controller.SideNavbar_Controller import SideNavbar_Controller
from config.App_Config import AppConfig
from widgets.LogFileTxt import logger
import sys
import os
from pathlib import Path
import json
from constants.Json_File_Path_Constants import json_paths

def get_base_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

def get_app_data_path():
    if getattr(sys, 'frozen', False):
        if os.name == 'nt':
            app_data = os.environ.get('APPDATA', '') or os.path.expanduser('~')
            data_path = os.path.join(app_data, 'BiomassCalculationTool')
        else:
            data_path = os.path.join(os.path.expanduser('~'), '.biomass_calc')
    else:
        data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app_data')
    os.makedirs(data_path, exist_ok=True)
    return data_path

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_user_data_path(relative_path):
    app_data_path = get_app_data_path()
    full_path = os.path.join(app_data_path, relative_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    return full_path

def initialize_json_files():
    logger.write("Initializing JSON files...")
    tree_params_data = open(get_resource_path("data/treeparameters.json"), 'r', encoding='utf-8').read()
    fresh_files = {
        "storage/localstorage.json": {},
        "data/treeparameters.json": json.loads(tree_params_data)
         
          }
    created_files = []
    for file_path, default_content in fresh_files.items():
        user_file_path = get_user_data_path(file_path)
        try:
            os.makedirs(os.path.dirname(user_file_path), exist_ok=True)
            with open(user_file_path, 'w', encoding='utf-8') as f:
                json.dump(default_content, f, indent=2, ensure_ascii=False)
            logger.write(f"   Created/Updated: {file_path}")
            created_files.append(file_path)
        except Exception as e:
            logger.write(f"   Error creating {file_path}: {str(e)}")

    for path_key, default in [
        (json_paths.CREATED_SPECIES_PATH, []),
        (json_paths.SELECTED_DATABASE_PATH, {}),
        (json_paths.CONNECTION_HISTORY_PATH, []),
    ]:
        full = get_user_data_path(path_key)
        if not os.path.exists(full):
            try:
                os.makedirs(os.path.dirname(full), exist_ok=True)
                with open(full, 'w', encoding='utf-8') as f:
                    json.dump(default, f, indent=2, ensure_ascii=False)
                logger.write(f"   Created: {path_key}")
                created_files.append(path_key)
            except Exception as e:
                logger.write(f"   Error creating {path_key}: {str(e)}")
        else:
            logger.write(f"   Preserved existing: {path_key}")

    logger.write(f"Initialized {len(created_files)} JSON files")


def setup_paths():
    if getattr(sys, 'frozen', False):
        project_root  = Path(sys._MEIPASS)
        app_data_path = get_app_data_path()
        logger.write(f"Running as compiled executable — data: {app_data_path}")
    else:
        project_root  = Path(__file__).parent
        app_data_path = get_app_data_path()
        logger.write(f"Running as script — data: {app_data_path}")
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    initialize_json_files()
    return project_root, app_data_path


def read_json_file(file_path):
    try:
        p = get_user_data_path(file_path)
        if os.path.exists(p):
            with open(p, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        logger.write(f"Error reading {file_path}: {e}")
    return None


def write_json_file(file_path, data):
    try:
        p = get_user_data_path(file_path)
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.write(f"Successfully wrote to {file_path}")
        return True
    except Exception as e:
        logger.write(f"Error writing to {file_path}: {e}")
        return False


# ── Splash screen ─────────────────────────────────────────────────────────────

def _build_splash(page: ft.Page) -> ft.Container:
    """Build a clean, on-brand splash screen."""
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    bg      = "#1A1A1A" if is_dark else "#FFFFFF"
    surface = "#222222" if is_dark else "#F8FAFC"
    border  = "#2E2E2E" if is_dark else "#E2E8F0"
    txt_p   = "#F5F5F5" if is_dark else "#0F172A"
    txt_s   = "#888888" if is_dark else "#64748B"

    return ft.Container(
        expand=True,
        bgcolor=bg,
        alignment=ft.alignment.center,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
            controls=[
                # ── Icon badge ──────────────────────────────────────────────
                ft.Container(
                    content=ft.Icon(ft.Icons.FOREST_ROUNDED, size=48, color="#16A34A"),
                    width=96, height=96,
                    bgcolor=ft.Colors.with_opacity(0.10, "#16A34A"),
                    border_radius=ft.border_radius.all(24),
                    border=ft.border.all(1, ft.Colors.with_opacity(0.2, "#16A34A")),
                    alignment=ft.alignment.center,
                ),
                ft.Container(height=28),

                # ── App name ────────────────────────────────────────────────
                ft.Text(
                    "Biomass Calculator",
                    size=26,
                    weight=ft.FontWeight.W_800,
                    color=txt_p,
                ),
                ft.Container(height=6),
                ft.Text(
                    "Professional Edition  ·  Version 1.0",
                    size=13,
                    color=txt_s,
                ),
                ft.Container(height=36),

                # ── Progress ring ───────────────────────────────────────────
                ft.Container(
                    content=ft.Column([
                        ft.ProgressRing(
                            color="#16A34A",
                            stroke_width=3,
                            width=28,
                            height=28,
                        ),
                        ft.Container(height=12),
                        ft.Text("Loading...", size=12, color=txt_s),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0, tight=True),
                ),
                ft.Container(height=48),

              
            ],
        ),
    )


def main(page: ft.Page):
    """Main entry point for the Biomass Calculation Tool."""
    try:
        project_root, app_data_path = setup_paths()
        logger.write("Application starting...")
        AppConfig(page).configure_page()
        logger.write("Page configured")

        async def show_splash_and_proceed():
            try:
                splash = _build_splash(page)
                page.add(splash)
                page.update()
                logger.write("Splash screen displayed")

                await asyncio.sleep(2.2)

                # Fade out
                splash.opacity = 0
                splash.animate_opacity = ft.Animation(280, ft.AnimationCurve.EASE_OUT)
                page.update()
                await asyncio.sleep(0.3)

                page.controls.clear()
                page.update()
                logger.write("Splash cleared — proceeding to EULA")

                DataManager().clear()
                eula_view = EULA_View(page=page, controller=None)
                eula_view.get_eula_view()
                page.update()
                logger.write("EULA view displayed")

            except Exception as e:
                logger.write(f"Error in splash_and_proceed: {e}")
                page.controls.clear()
                page.add(ft.Container(
                    expand=True,
                    alignment=ft.alignment.center,
                    content=ft.Column([
                        ft.Icon(ft.Icons.ERROR_OUTLINE_ROUNDED, size=48,
                                color="#DC2626"),
                        ft.Container(height=12),
                        ft.Text("Application Error", size=20,
                                weight=ft.FontWeight.W_700, color="#DC2626"),
                        ft.Text(str(e), size=13,
                                color="#888888",
                                text_align=ft.TextAlign.CENTER),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0, tight=True),
                ))
                page.update()

        page.run_task(show_splash_and_proceed)

    except Exception as e:
        logger.write(f"Fatal error in main: {e}")
        page.add(ft.Text(f"Fatal Error: {e}", color="#DC2626"))
        page.update()


if __name__ == "__main__":
    ft.app(target=main)