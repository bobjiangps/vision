from lib.compiled.levenshtein import compute

DEGREE = 1


def least(inspect, expect):
    if not isinstance(inspect, list):
        return None
    key = None
    value = None
    for i in inspect:
        result = compute(i, expect)
        if key:
            if result < value:
                key = i
                value = result
        else:
            key = i
            value = result
    return key


def qualified(inspect, expect):
    if isinstance(inspect, list):
        keys = []
        top = None
        for i in inspect:
            result = compute(i, expect)
            if result == DEGREE:
                keys.append(i)
                if not top:
                    top = i
        return top, keys
    elif compute(inspect, expect) == DEGREE:
        return inspect
    else:
        return False
