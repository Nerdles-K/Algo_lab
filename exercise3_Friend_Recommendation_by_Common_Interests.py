import math

def cosine_similarity(userA, userB):
    dot_product = 0
    normA = 0
    normB = 0
    
    for i in range(len(userA)):
        dot_product += userA[i] * userB[i]
        normA += userA[i] ** 2
        normB += userB[i] ** 2
        
    normA = math.sqrt(normA)
    normB = math.sqrt(normB)
    
    if normA == 0 or normB == 0:
        return 0
    return dot_product / (normA * normB)

def find_top_k(target_user_id, matrix, friends_set, k=2):
    scores = []
    target_interests = matrix[target_user_id]
    
    for user_id in range(len(matrix)):
        if user_id != target_user_id and user_id not in friends_set:
            score = cosine_similarity(target_interests, matrix[user_id])
            scores.append((user_id, score))
            
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:k]

def collaborative_filtering(target_user_id, matrix, top_k_users):
    num_interests = len(matrix[0])
    predictions = [0.0] * num_interests
    total_weight = 0
    
    for rec_user_id, weight in top_k_users:
        total_weight += weight
        for i in range(num_interests):
            if matrix[target_user_id][i] == 0:
                predictions[i] += weight * matrix[rec_user_id][i]
                
    if total_weight > 0:
        for i in range(num_interests):
            predictions[i] = round(predictions[i] / total_weight, 2)
            
    return predictions

interests = ["Music", "Sports", "Tech", "Fashion", "Travel", "Food"]
matrix = [
    [10, 0, 8, 2, 5, 7], 
    [9, 1, 7, 3, 6, 8],  
    [2, 9, 1, 8, 3, 0]   
]

top_k = find_top_k(0, matrix, set())
preds = collaborative_filtering(0, matrix, top_k)

print(f"Interest Recommendations for User 0: {preds}")