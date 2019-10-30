from os.path import expanduser

def apath(path):
    return path.replace('~', expanduser('~'), 1)
    
