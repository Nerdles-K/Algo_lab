def first_unique_char(s):
    
    if not s: 
        return -1

    freq = {}

    for c in s:
        if c in freq:
            freq[c] += 1
        else:
            freq[c] = 1

    for i in range(len(s)):
        c = s[i]
        if freq[c] == 1:
            return i

    return -1