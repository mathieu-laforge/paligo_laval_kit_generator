def has_numbers(inputString: str):
    """
    # Has numbers
    Verify that the input string contains numbers

    Parameters
    ----------
    inputString : (str)
        any string

    Returns
    -------
    (bool)
        True if the input string contains numbers
        False otherwise
    """
    return any(char.isdigit() for char in inputString)