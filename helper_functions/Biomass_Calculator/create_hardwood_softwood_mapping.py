def create_hardwood_softwood_species_code_mapping(hardwood_species_codes: list, softwood_species_codes: list) -> dict:
        """Create a mapping of species codes to their type (hardwood or softwood)."""
        mapping = {}
        for code in hardwood_species_codes:
            mapping[code] = "hardwood"
        for code in softwood_species_codes:
            mapping[code] = "softwood"
        return mapping