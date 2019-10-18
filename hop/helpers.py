from os.path import expanduser

def full_path(path):
    """converts a relative path with user home (~) to an absolute path

    Parameters
    ----------
    path : str, required
        a filesystem path

    Raises
    ------
    No specific exceptions

    Returns
    -------
    abs_path : str
        the converted absolute path
    """
    abs_path = path.replace('~', expanduser('~'), 1)
    return abs_path

