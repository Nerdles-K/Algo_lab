class FollowerMatrix:
    def __init__(self, max_users, actual_user_count):
        self.size = max_users 
        self.user_count = actual_user_count
        # Default: False (no follow relationship)
        self.matrix = [[False for _ in range(max_users)] for _ in range(max_users)]

    def _is_valid(self, user_id):
        return 1 <= user_id <= self.size

    def follow(self, follower, followee):
        if self._is_valid(follower) and self._is_valid(followee):
            self.matrix[follower - 1][followee - 1] = True

    def unfollow(self, follower, followee):
        if self._is_valid(follower) and self._is_valid(followee):
            self.matrix[follower - 1][followee - 1] = False

    def is_following(self, follower, followee):
        if self._is_valid(follower) and self._is_valid(followee):
            return self.matrix[follower - 1][followee - 1]
        return False

    def get_following(self, user):
        if not self._is_valid(user): return []
        
        result = []
        row_idx = user - 1
        for col_idx in range(self.size):
            if self.matrix[row_idx][col_idx]:
                result.append(col_idx + 1)
        return result

    def get_followers(self, user):
        if not self._is_valid(user): return []
        
        result = []
        col_idx = user - 1
        for row_idx in range(self.size):
            if self.matrix[row_idx][col_idx]:
                result.append(row_idx + 1)
        return result

    def get_mutual_follows(self):
        pairs = []
        for i in range(self.size):
            for j in range(i + 1, self.size):
                # i follows j AND j follows i
                if self.matrix[i][j] and self.matrix[j][i]:
                    pairs.append((i + 1, j + 1))
        return pairs

    def get_influence_score(self, user):
        """Score = (Followers + Following) / Total_Users"""
        if not self._is_valid(user): return 0.0
        
        following_count = len(self.get_following(user))
        followers_count = len(self.get_followers(user))
        
        return (following_count + followers_count) / self.user_count

# === Edge Test (Exercise 4) ===
print("\n=== Exercise 4: Adjacency Matrix ===")
# N=3
matrix = FollowerMatrix(max_users=3, actual_user_count=3)

# User 1 -> 2
matrix.follow(1, 2)
# User 2 -> 1, 3
matrix.follow(2, 1)
matrix.follow(2, 3)

# Print Matrix
print("Current Matrix State:")
for row in matrix.matrix:
    print([int(x) for x in row])

print(f"User 1 Following: {matrix.get_following(1)}") # [2]
print(f"User 2 Followers: {matrix.get_followers(2)}") # [1]

mutuals = matrix.get_mutual_follows()
print(f"Mutual Follows: {mutuals}") # [(1, 2)]

# User 1: (1+1)/3 = 0.66
print(f"Influence User 1: {matrix.get_influence_score(1):.2f}") 
# User 2: (2+1)/3 = 1.00
print(f"Influence User 2: {matrix.get_influence_score(2):.2f}")