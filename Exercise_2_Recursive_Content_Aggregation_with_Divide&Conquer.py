from datetime import datetime

class Post:
    def __init__(self, post_id, user_id, content_preview, timestamp, likes, comments, shares):
        self.post_id = post_id
        self.user_id = user_id
        self.content_preview = content_preview
        self.timestamp = timestamp
        self.likes = likes
        self.comments = comments
        self.shares = shares
        self.engagement_score = self.calculate_engagement()

    def calculate_engagement(self):
        return (self.likes * 1) + (self.comments * 2) + (self.shares * 3)

def max_engagement(posts, left, right):
    if left == right:
        return posts[left].engagement_score

    mid = (left + right) // 2
    max_left  = max_engagement(posts, left, mid)
    max_right = max_engagement(posts, mid + 1, right)

    if max_left > max_right:
        return max_left
    else:
        return max_right

def sum_engagement(posts, left, right):
    if left == right:
        return posts[left].engagement_score

    mid = (left + right) // 2
    return sum_engagement(posts, left, mid) + sum_engagement(posts, mid + 1, right)

def average_engagement(posts, left, right):
    total = sum_engagement(posts, left, right)
    count = (right - left) + 1
    return total / count

def count_above_threshold(posts, left, right, threshold):
    if left == right:
        if posts[left].engagement_score > threshold:
            return 1
        else:
            return 0

    mid = (left + right) // 2
    return (count_above_threshold(posts, left, mid, threshold) +
            count_above_threshold(posts, mid + 1, right, threshold))

def merge_sort_by_engagement(posts, left, right):
    if left < right:
        mid = (left + right) // 2
        merge_sort_by_engagement(posts, left, mid)
        merge_sort_by_engagement(posts, mid + 1, right)
        merge(posts, left, mid, right)

def merge(posts, left, mid, right):
    left_part  = posts[left : mid + 1]
    right_part = posts[mid + 1 : right + 1]

    i = 0
    j = 0
    k = left

    while i < len(left_part) and j < len(right_part):
        if left_part[i].engagement_score <= right_part[j].engagement_score:
            posts[k] = left_part[i]
            i += 1
        else:
            posts[k] = right_part[j]
            j += 1
        k += 1

    while i < len(left_part):
        posts[k] = left_part[i]
        i += 1
        k += 1

    while j < len(right_part):
        posts[k] = right_part[j]
        j += 1
        k += 1

def find_peak_hour(likes, left, right):
    mid = (left + right) // 2

    if (mid == 0 or likes[mid] >= likes[mid - 1]) and \
       (mid == 23 or likes[mid] >= likes[mid + 1]):
        return mid

    elif mid < 23 and likes[mid + 1] > likes[mid]:
        return find_peak_hour(likes, mid + 1, right)

    else:
        return find_peak_hour(likes, left, mid - 1)

posts = [
    Post(1, "u1", "Post one",   datetime(2024, 1, 1), likes=50,  comments=25, shares=25),
    Post(2, "u2", "Post two",   datetime(2024, 1, 2), likes=100, comments=60, shares=40),
    Post(3, "u3", "Post three", datetime(2024, 1, 3), likes=30,  comments=15, shares=10),
    Post(4, "u4", "Post four",  datetime(2024, 1, 4), likes=80,  comments=50, shares=30),
]

n = len(posts) - 1

print("=== Engagement Scores ===")
for p in posts:
    print(f"  Post{p.post_id}: {p.engagement_score}")

print(f"\nMax engagement:            {max_engagement(posts, 0, n)}")
print(f"Sum engagement:            {sum_engagement(posts, 0, n)}")
print(f"Average engagement:        {average_engagement(posts, 0, n):.2f}")
print(f"Count above threshold 200: {count_above_threshold(posts, 0, n, 200)}")

merge_sort_by_engagement(posts, 0, n)
print("\nSorted by engagement score:")
for p in posts:
    print(f"  Post{p.post_id}: {p.engagement_score}")

hourly_likes = [5, 8, 12, 25, 30, 28, 15, 10, 6, 4, 3, 2,
                1, 2, 3,  5,  8, 12, 20, 18, 14, 9, 6, 3]
peak = find_peak_hour(hourly_likes, 0, 23)
print(f"\nPeak hour: hour {peak} ({hourly_likes[peak]} likes)")