from os.path import expanduser
from re import sub
import collections.abc

def apath(path):
    return path.replace('~', expanduser('~'), 1)

# check if check_dir is the same directory or a subdirectory of ref_dir
# set allow_match to false if you want to check if only a subdirectory and not same 
# TODO find a better solution or us os.path to make sure paths also exist
def issubdir(check_dir, ref_dir, allow_match = True):
    if allow_match:
        return (f'{check_dir}/' == f'{ref_dir}/') or (check_dir.startswith(f'{ref_dir}/'))
    else:
        return check_dir.startswith(f'{ref_dir}/')

def mergedicts(dict1, dict2):
    for k, v in dict2.items():
        if isinstance(v, collections.abc.Mapping):
            dict1[k] = mergedicts(dict1.get(k, {}), v)
        else:
            dict1[k] = v
    return dict1

def camelcase(s):
    s = sub(r"(_|-)+", " ", s).title().replace(" ", "").replace("*","")

    return ''.join([s[0].lower(), s[1:]])

def snake_case(s):
  return '_'.join(
    sub('([A-Z][a-z]+)', r' \1',
    sub('([A-Z]+)', r' \1',
    s.replace('-', ' '))).split()).lower()
