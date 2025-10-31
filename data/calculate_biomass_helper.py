
def round_sig(x, sig=4):
    try:
        return float(f"{x:.{sig}g}")
    except (ValueError, TypeError):
        return x  # fallback if x is not a number

def calculate_wood(bwood1, dbh, bwood2):
    return round_sig(bwood1 * dbh ** bwood2)

def calculate_bark(bbark1, dbh, bbark2):
    return round_sig(bbark1 * dbh ** bbark2)

def calculate_foilage(bfoilage1, dbh, bfoilage2):
    return round_sig(bfoilage1 * dbh ** bfoilage2)

def calculate_branches(bbranches1, dbh, bbranches2):
    return round_sig(bbranches1 * dbh ** bbranches2)
