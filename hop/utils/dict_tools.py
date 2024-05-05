from functools import reduce


def dig(_dict, *keys, default=None):
    return (
        reduce(lambda d, key: d.get(key, default)
        if isinstance(d, dict) else default, keys, _dict)
    )
