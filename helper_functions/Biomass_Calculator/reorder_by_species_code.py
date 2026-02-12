
def reorder_by_species_code(data):
    """Reorder the DataFrame by 'speciescode' in ascending order."""
    if 'species' in data.columns:
        return data.sort_values(by='species').reset_index(drop=True)
    return data