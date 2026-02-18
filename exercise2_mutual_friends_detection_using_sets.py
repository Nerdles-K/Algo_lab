class SocialNetworkSets:
    def __init__(self):
        self.graph = {}

    def add_user_friends(self, user_id, friends_set):
        self.graph[user_id] = set(friends_set)

    @staticmethod
    def get_intersection(set1, set2):
        mutual_set = set()
        if len(set1) < len(set2):
            smaller_set = set1
            larger_set = set2
        else:
            smaller_set = set2
            larger_set = set1
            
        # FOR EACH element IN SmallerSet
        for element in smaller_set:
            # IF element IN LargerSet
            if element in larger_set:
                # ADD element to MutualSet
                mutual_set.add(element)
                
        return mutual_set

    @staticmethod
    def get_difference(set1, set2):
        result_set = set()
        
        # FOR EACH element IN set1
        for element in set1:
            # IF element not IN set2
            if element not in set2:
                result_set.add(element)
                
        return result_set

    @staticmethod
    def get_union(set1, set2):
        union_set = set(set1) 
        
        for element in set2:
                union_set.add(element)
                
        return union_set

    @staticmethod
    def calculate_jaccard(set1, set2):
        intersection = SocialNetworkSets.get_intersection(set1, set2)
        union = SocialNetworkSets.get_union(set1, set2)
        
        if len(union) == 0: 
            return 0.0
        return len(intersection) / len(union)


    def get_suggestions(self, user_id):
        if user_id not in self.graph: return set()
        
        my_friends = self.graph[user_id]
        friends_of_friends_pool = set()

        for friend in my_friends:
            if friend in self.graph:
                their_friends = self.graph[friend]
                friends_of_friends_pool = friends_of_friends_pool | their_friends

        suggestions = friends_of_friends_pool - my_friends
        
        suggestions.discard(user_id)
        
        return suggestions

# === Edge Test (Exercise 2) ===
print("=== Exercise 2: Sets & Mutual Friends ===")
sn = SocialNetworkSets()

user_a_friends = {101, 102, 103, 104, 105}
user_b_friends = {103, 104, 106, 107, 108}

sn.add_user_friends("A", user_a_friends)
sn.add_user_friends("B", user_b_friends)

mutual = sn.get_intersection(user_a_friends, user_b_friends)
unique_a = sn.get_difference(user_a_friends, user_b_friends)
unique_b = sn.get_difference(user_b_friends, user_a_friends)
jaccard = sn.calculate_jaccard(user_a_friends, user_b_friends)

print(f"User A Friends: {user_a_friends}")
print(f"User B Friends: {user_b_friends}")
print(f"1. Mutual Friends: {mutual}")       # {103, 104}
print(f"2. Unique to A: {unique_a}")        # {101, 102, 105}
print(f"3. Jaccard Coefficient: {jaccard}") # 0.25 (2/8)

# Suggest 999, B
sn.add_user_friends(103, {"A", "B", 999}) 
print(f"4. Suggestions for A: {sn.get_suggestions('A')}") 
