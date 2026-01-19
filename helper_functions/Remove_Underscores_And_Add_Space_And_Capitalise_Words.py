
def Remove_Underscores_And_Add_Space_And_Capitalise_Words(text: str) -> str:
    """Helper function to format nav item text."""
    return text.replace("_", " ").title() # capitalise each word