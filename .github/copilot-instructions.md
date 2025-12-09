<!-- .github/copilot-instructions.md: Guidance for AI coding agents working on this repo -->
# Quick agent instructions — Biomass-Calculation-Tool

This file captures the minimal, actionable knowledge an AI coding agent needs to be productive in this Python/Flet UI app.

- Entrypoint: `main.py` — app uses Flet (`ft.app(target=main)`). The app shows the EULA view first (`controller/eula_menu.py`).
- UI architecture: MVC-ish separation:
  - `controller/` — controller classes / event handlers (e.g. `Main_Controller.py`). Controllers drive state changes and rebuild view fragments.
  - `model/` — simple models (e.g. `Main_Model.py`, species models). Controllers call model methods.
  - `views/` — Flet view builders that assemble UI and call controllers.
  - `widgets/` — reusable Flet widgets (cards, dialogs, inputs). Prefer adding shared UI primitives here.
  - `data/` — data helpers and persistence (`data_manager.py`, `import_dataset_helper.py`, `treeparameters.json`).

- Persistence and data flow:
  - Runtime state stored via the singleton `DataManager` in `data/data_manager.py`. It reads/writes `storage/localstorage.json`.
  - Import pipeline: `data/import_dataset_helper.py::csv_to_json(csv_file)` reads CSV (commas or tabs), writes to `DataManager` and calls `manager.add_parameters()` to merge `data/treeparameters.json` entries.
  - Species matching uses `SpecCommon` (case-insensitive key) — merging avoids duplicating `SpecCommon`.

- Patterns & conventions to follow when modifying code:
  - Controllers update models, then call a local refresh method to rebuild small parts of the view (see `Main_Controller._refresh_view`). Keep that separation.
  - Views register controls with controllers via explicit initializer methods (example: `initialize_view_controls(selected_text, cards_row)` in `Main_Controller`). When adding new controls, ensure the view registers them with the controller.
  - Widgets return Flet controls (not raw HTML); treat widgets as composable Flet factories. Place new UI elements under `widgets/`.
  - DataManager is a thread-safe singleton — use DataManager() to access persistent data; prefer its helper methods (`get_all`, `set_all`, `add_entry`, `add_parameters`, `clear`).

- Important files to open first when making changes:
  - `main.py` — app entry and lifecycle (on_close behavior clears local storage by default).
  - `controller/Main_Controller.py` — demonstrates controller → model → view flow.
  - `data/data_manager.py` — persistence, singleton behavior, parameter merging.
  - `data/import_dataset_helper.py` — CSV import behavior (delimiter detection, field trimming).
  - an example widget: `widgets/Display_Warning_Dialog.py` — complex dialog UI patterns (Tabs, ListView, parsing/formatting functions).

- Run & debug notes (discoverable from repo):
  - Run the app locally: `python main.py` (requires Flet runtime). Use the Python process/IDE to set breakpoints in controllers/views.
  - Import via script: in a Python REPL/script: `from data.import_dataset_helper import csv_to_json; csv_to_json('path/to/file.csv')` — this writes `storage/localstorage.json` and merges parameters.
  - Persistent files: `storage/localstorage.json` and `data/treeparameters.json` — tests and UI depend on these paths.

- Project-specific gotchas & examples:
  - Field names used throughout: `DBH`, `Height`, `SpecCommon`, `Species`, `Plot`, `SubPlot`, `TreeStatus`, `Tree`. Many UI formatting/parsing functions assume these keys exist.
  - DBH/Height validation: tree measurement ranges are enforced in widget code (see `_is_invalid_tree_measurement` in `widgets/Display_Warning_Dialog.py`). When altering validation, update both UI messages and any data import normalization.
  - Controllers often rebuild parts of the UI by recreating control lists and calling `.update()` (see `_refresh_view`). Avoid direct mutation of model data without calling the proper refresh flow.

- External dependencies (inferred):
  - `flet` — UI framework used across the project.
  - `pandas` is referenced in widgets for NaN checks. Add these to `requirements.txt` if you create one.

- When editing the repo, prefer small, focused commits that:
  1) change controller or model behavior, 2) update the corresponding view/widget, 3) run the app and verify UI interaction. Keep changes grouped around the MVC boundary.

If any section is unclear or you'd like me to expand examples (e.g., how to add a new Controller+View pair or prepare a requirements.txt), tell me which area and I'll iterate. 
