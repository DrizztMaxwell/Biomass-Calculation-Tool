#calculate_biomass_helper
def round_sig(x, sig=4):
    try:
        return float(f"{x:.{sig}g}")
    except (ValueError, TypeError):
        return x  # fallback if x is not a number


def safe_float(value):
    """Safely convert to float; returns None if invalid or placeholder."""
    if value in [None, "", "-", "NA", "N/A"]:
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def calculate_component(formula_func, *args):
    """General helper: runs formula_func if all args valid, else returns 'NotAv'."""
    if any(a is None for a in args):
        return "NotAv"
    try:
        return round_sig(formula_func(*args))
    except Exception:
        return "NotAv"


# -------------------------------
# DBH-only equations
# -------------------------------

def calculate_wood(bwood1, dbh, bwood2):
    bwood1, dbh, bwood2 = map(safe_float, [bwood1, dbh, bwood2])
    return calculate_component(lambda a, b, c: a * b ** c, bwood1, dbh, bwood2)


def calculate_bark(bbark1, dbh, bbark2):
    bbark1, dbh, bbark2 = map(safe_float, [bbark1, dbh, bbark2])
    return calculate_component(lambda a, b, c: a * b ** c, bbark1, dbh, bbark2)


def calculate_foliage(bfoliage1, dbh, bfoliage2):
    bfoliage1, dbh, bfoliage2 = map(safe_float, [bfoliage1, dbh, bfoliage2])
    return calculate_component(lambda a, b, c: a * b ** c, bfoliage1, dbh, bfoliage2)


def calculate_branches(bbranches1, dbh, bbranches2):
    bbranches1, dbh, bbranches2 = map(safe_float, [bbranches1, dbh, bbranches2])
    return calculate_component(lambda a, b, c: a * b ** c, bbranches1, dbh, bbranches2)


# -------------------------------
# DBH + Height equations
# -------------------------------

def calculate_wood_height(bhwood1, dbh, bhwood2, httot, bhwood3):
    bhwood1, dbh, bhwood2, httot, bhwood3 = map(safe_float, [bhwood1, dbh, bhwood2, httot, bhwood3])
    return calculate_component(lambda a, b, c, d, e: a * b ** c * d ** e, bhwood1, dbh, bhwood2, httot, bhwood3)


def calculate_bark_height(bhbark1, dbh, bhbark2, httot, bhbark3):
    bhbark1, dbh, bhbark2, httot, bhbark3 = map(safe_float, [bhbark1, dbh, bhbark2, httot, bhbark3])
    return calculate_component(lambda a, b, c, d, e: a * b ** c * d ** e, bhbark1, dbh, bhbark2, httot, bhbark3)


def calculate_foliage_height(bhfoliage1, dbh, bhfoliage2, httot, bhfoliage3):
    bhfoliage1, dbh, bhfoliage2, httot, bhfoliage3 = map(safe_float, [bhfoliage1, dbh, bhfoliage2, httot, bhfoliage3])
    return calculate_component(lambda a, b, c, d, e: a * b ** c * d ** e, bhfoliage1, dbh, bhfoliage2, httot, bhfoliage3)


def calculate_branches_height(bhbranches1, dbh, bhbranches2, httot, bhbranches3):
    bhbranches1, dbh, bhbranches2, httot, bhbranches3 = map(safe_float, [bhbranches1, dbh, bhbranches2, httot, bhbranches3])
    return calculate_component(lambda a, b, c, d, e: a * b ** c * d ** e, bhbranches1, dbh, bhbranches2, httot, bhbranches3)
