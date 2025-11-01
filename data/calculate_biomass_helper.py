#calculate_biomass_helper
def round_sig(x, sig=4):
    try:
        return float(f"{x:.{sig}g}")
    except (ValueError, TypeError):
        return x  # fallback if x is not a number

def calculate_wood(bwood1, dbh, bwood2):
    return round_sig(bwood1 * dbh ** bwood2)

def calculate_bark(bbark1, dbh, bbark2):
    return round_sig(bbark1 * dbh ** bbark2)

def calculate_foliage(bfoliage1, dbh, bfoliage2):
    return round_sig(bfoliage1 * dbh ** bfoliage2)

def calculate_branches(bbranches1, dbh, bbranches2):
    return round_sig(bbranches1 * dbh ** bbranches2)

def calculate_wood_height(bhwood1, dbh, bhwood2, httot, bhwood3):
    return round_sig(bhwood1 * dbh ** bhwood2 * httot ** bhwood3)

def calculate_bark_height(bhbark1, dbh, bhbark2, httot, bhbark3):
    return round_sig(bhbark1 * dbh ** bhbark2 * httot ** bhbark3)

def calculate_foliage_height(bhfoliage1, dbh, bhfoliage2, httot, bhfoliage3):
    return round_sig(bhfoliage1 * dbh ** bhfoliage2 * httot ** bhfoliage3)

def calculate_branches_height(bhbranches1, dbh, bhbranches2, httot, bhbranches3):
    return round_sig(bhbranches1 * dbh ** bhbranches2 * httot ** bhbranches3)