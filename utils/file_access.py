import os

def file_access(file: str, extention: str | None):
    """
    # File Access
    Access file with simple relative path
    
    Parameters
    ----------
    file : str
        relative path to file
    extension : str 
        file extension
    
    Returns
    -------
    str
        the system path to file
    """
    if extention == None:
        extention = ""
        file_dir = os.path.dirname(os.path.realpath('__file__'))
        file = os.path.join(file_dir, file)
    else:
        x = "."+extention
        file_dir = os.path.dirname(os.path.realpath('__file__'))
        file = os.path.join(file_dir, file+x)
    return file
