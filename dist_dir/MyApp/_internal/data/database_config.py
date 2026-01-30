# database_config.py

import pyodbc
import glob
import os

def get_sql_server_odbc_driver() -> str:
    """
    Returns the newest installed SQL Server ODBC driver.
    Raises RuntimeError if none found.
    """
    drivers = pyodbc.drivers()

    # Filter SQL Server drivers and sort by version number
    sql_drivers = [
        d for d in drivers
        if "ODBC Driver" in d and "SQL Server" in d
    ]

    if not sql_drivers:
        raise RuntimeError("No SQL Server ODBC drivers found.")

    # Sort by version number (e.g., 18 > 17 > 13)
    sql_drivers.sort(
        key=lambda d: int("".join(filter(str.isdigit, d))),
        reverse=True
    )

    return sql_drivers[0]


def get_mssql_data_path() -> str | None:
    """
    Attempts to locate the MSSQL SQLEXPRESS DATA directory
    under Program Files (32-bit and 64-bit). Returns the first match found,
    or None if not found.
    """
    program_files_dirs = [os.environ.get("ProgramFiles"), os.environ.get("ProgramFiles(x86)")]
    for pf in program_files_dirs:
        if not pf:
            continue
        # Search for folders like MSSQL17.SQLEXPRESS
        pattern = os.path.join(pf, "Microsoft SQL Server", "MSSQL*.SQLEXPRESS", "MSSQL", "DATA")
        matches = glob.glob(pattern)
        if matches:
            return matches[0]  # Return the first DATA directory found
    return None
