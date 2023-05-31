from .config import (
    decremental
)

def judge(result, pos, j, track):
    if track not in decremental:
        return (result[pos][9] > result[j][9]) or (result[pos][9] == result[j][9] and result[pos][8] < result[j][8])
    else:
        return (result[pos][9] < result[j][9]) or (result[pos][9] == result[j][9] and result[pos][8] < result[j][8])

def score_sort(result, track):
    for pos in range(len(result)):
        for j in range(pos+1, len(result)):
            if judge(result, pos, j, track):
                tmp = result[pos].copy()
                result[pos] = result[j].copy()
                result[j] = tmp