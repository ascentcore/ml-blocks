# TODO in the future maybe come up with a cleaner solution

def smaller_then(variable, threshold) -> bool:
    if float(variable) < threshold:
        return True
    return False


def bigger_then(variable, threshold) -> bool:
    if float(variable) > threshold:
        return True
    return False
