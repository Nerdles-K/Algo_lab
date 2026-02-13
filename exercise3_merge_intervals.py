from typing import List

def merge(intervals: List[List[int]]) -> List[List[int]]:
    intervals.sort(key=lambda x: x[0])
    merged = []
    for interval in intervals:
        if not merged or merged[-1][1] < interval[0]:
            merged.append(interval)
        else:
            merged[-1][1] = max(merged[-1][1], interval[1])
    return merged

# Edge Tests
print(merge([[1,3],[2,6],[15,18],[8,10]]))  # [[1,6],[8,10],[15,18]]
print(merge([[1,4],[4,5]]))  # [[1,5]]
print(merge([[1,4],[0,4]]))  # [[0,4]]
print(merge([[1,3],[2,4],[3,5]]))  # [[1,5]]
print(merge([[1,4]]))  # [[1,4]]
print(merge([[1,5],[5,6]]))  # [[1,6]]