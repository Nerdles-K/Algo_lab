import math

def analyze_friend_request(text):
    upper_count = 0
    punc_count = 0
    alpha_count = 0
    has_spam = False
    
    for i in range(len(text)):
        char = text[i]
        
        if char.isupper():
            upper_count += 1 
        if char in "!?":
            punc_count += 1 
        if char.isalpha():
            alpha_count += 1
            
        if i >= 3:
            if text[i] == text[i-1] == text[i-2] == text[i-3]:
                has_spam = True

    caps_ratio = upper_count / alpha_count if alpha_count > 0 else 0

    if caps_ratio >= 0.6 or punc_count >= 5:
        category = "AGGRESSIVE" 
    elif caps_ratio >= 0.3 or punc_count >= 3:
        category = "URGENT" 
    else:
        category = "CALM"

    return {
        "classification": category,
        "caps_ratio": round(caps_ratio, 2),
        "punctuation": punc_count,
        "spam_detected": has_spam
    }

print(analyze_friend_request("PLEASE ACCEPT MY REQUEST!!!"))