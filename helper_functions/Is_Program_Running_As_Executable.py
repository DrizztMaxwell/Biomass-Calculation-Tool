import sys

def is_program_running_as_executable():
    """Returns True if running as .exe, False if running as script"""
    return getattr(sys, 'frozen', False)