# Temporary Array
def rotate_array_temp(Vec, k):
    n = len(Vec)
    temp = [0] * n
    for i in range(n):
        temp[(i + k) % n] = Vec[i]
    for i in range(n):
        Vec[i] = temp[i]
    return Vec

# Rotate one by one
def rotate_one_by_one(Vec, k):
    n = len(Vec)
    k = k % n
    for i in range(k):
        last = Vec[-1]
        for j in range(n - 1, 0, -1):
            Vec[j] = Vec[j - 1]
        Vec[0] = last
    return Vec

# Reverse Segments Method
def reverse_segment(Vec, k):
    n = len(Vec)
    k = k % n
    Vec.reverse()
    Vec[:k] = reversed(Vec[:k])
    Vec[k:] = reversed(Vec[k:])
    return Vec

# Edge Tests
print(rotate_array_temp([1,2,3,4,5], 2)) # [4,5,1,2,3]
print(rotate_one_by_one([1,2,3,4,5], 5)) # [1,2,3,4,5]
print(reverse_segment([1,2,3,4,5], 3)) # [3,4,5,1,2]
print(reverse_segment([1,2,3,4,5], 0)) # [1,2,3,4,5]
print(reverse_segment([1], 3)) # [1]