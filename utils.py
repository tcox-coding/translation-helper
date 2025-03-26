from functools import reduce

def deref_multi(data, keys):
    return reduce(lambda d, key: d[key], keys, data)