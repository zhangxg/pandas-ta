import numpy as np
import pandas as pd

PEAK = 1
VALLEY = -1


def zigzag(
    s: pd.Series,
    up: float,
    down: float,
    include_end: bool = True,
    eagerly: bool = True,
):

    t = len(s)
    s = s.values
    pivots = np.zeros(t, dtype=np.int_)

    down = -down if down > 0 else down
    up += 1
    down += 1
    # check the starting trend
    initial_pivot = VALLEY if s[1] > s[0] else PEAK
    trend = -initial_pivot
    pivots[0] = initial_pivot

    i_last_pivot = 0
    v_last_pivot = s[0]

    for i in range(1, t):
        x = s[i]
        r = x / v_last_pivot

        if trend == -1:
            if r >= up:
                pivots[i_last_pivot] = trend
                trend = PEAK
                i_last_pivot = i
                v_last_pivot = x
            elif x < v_last_pivot:
                i_last_pivot = i
                v_last_pivot = x
        else:
            if r <= down:
                pivots[i_last_pivot] = trend
                trend = VALLEY
                i_last_pivot = i
                v_last_pivot = x
            elif x > v_last_pivot:
                i_last_pivot = i
                v_last_pivot = x
    # handle the end
    if include_end:
        if eagerly:
            if i_last_pivot > 0 and i_last_pivot < t - 1:
                pivots[i_last_pivot] = trend
                pivots[t - 1] = -trend
            else:
                pivots[t - 1] = trend
        else:
            if i_last_pivot == t - 1:
                pivots[i_last_pivot] = trend
            elif pivots[t - 1] == 0:
                pivots[t - 1] = -trend
    return pivots


zigzag.__doc__ = """Zigzag 

this is revised version of https://github.com/jbn/ZigZag



"""
