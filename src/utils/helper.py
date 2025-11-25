
def is_not_list_of_strings(variable):
    # Check if it's not a list at all
    if not isinstance(variable, list):
        return True

    # If it is a list, check if any element is not a string
    for item in variable:
        if not isinstance(item, str):
            return True

    # If it's a list and all elements are strings, then it IS a list of strings
    return False