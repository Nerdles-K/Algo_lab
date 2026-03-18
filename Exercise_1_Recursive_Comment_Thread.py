class CommentNode:
    def __init__(self, comment_id, user_id, content, timestamp, likes):
        self.comment_id = comment_id
        self.user_id = user_id    
        self.content = content[:100] 
        self.timestamp = timestamp   
        self.likes = likes           
        self.replies = []            

    def add_reply(self, reply_node):
        self.replies.append(reply_node)

def display_thread(comment, level=0):
    print("  " * level + comment.content)
    
    for reply in comment.replies:
        display_thread(reply, level + 1)

def count_total_comments(comment):
    count = 1  
    for reply in comment.replies:
        count += count_total_comments(reply)
    return count

def total_likes(comment):
    total = comment.likes
    for reply in comment.replies:
        total += total_likes(reply)
    return total

def find_deepest_reply(comment):
    if not comment.replies:
        return 0
    
    max_depth = 0
    for reply in comment.replies:
        depth = find_deepest_reply(reply)
        if depth > max_depth:
            max_depth = depth
            
    return 1 + max_depth

def search_by_user(user_id, comment):
    results = []
    
    if comment.user_id == user_id:
        results.append(comment)
        
    for reply in comment.replies:
        results.extend(search_by_user(user_id, reply))
        
    return results

def contains_keyword(keyword, comment):
    if keyword in comment.content:
        return True
        
    for reply in comment.replies:
        if contains_keyword(keyword, reply):
            return True
            
    return False

def delete_comment(comment_id, thread):
    if thread.comment_id == comment_id:
        return None
    
    new_replies = []
    for reply in thread.replies:
        if reply.comment_id != comment_id:
            processed_reply = delete_comment(comment_id, reply)
            if processed_reply is not None:
                new_replies.append(processed_reply)
                
    thread.replies = new_replies
    return thread


def run_edge_case_tests():
    print("=== 1. Structural Edge Cases ===")
    
    # Test 1.1: single comment with no replies
    lone_wolf = CommentNode(1, "user_A", "Just a single comment", "2026-03-18", 5)
    print("Test 1.1 - Total Comments:", count_total_comments(lone_wolf), "| Expected: 1")
    print("Test 1.1 - Max Depth:", find_deepest_reply(lone_wolf), "| Expected: 0")
    
    # Test 1.2: Deep nested replies
    head = CommentNode(10, "user_B", "Level 0", "2026-03-18", 0)
    current = head
    for i in range(1, 11): 
        new_node = CommentNode(10+i, "user_B", f"Level {i}", "2026-03-18", 0)
        current.add_reply(new_node)
        current = new_node
    print("Test 1.2 (Linked List) - Max Depth:", find_deepest_reply(head), "| Expected: 10")
    print("Test 1.2 (Linked List) - Total Comments:", count_total_comments(head), "| Expected: 11")

    print("\n=== 2. Search Edge Cases ===")

    # Test 2.1: keyword and user that do not exist
    ghost_search = search_by_user("ghost_user", lone_wolf)
    print("Test 2.1 (Ghost User) - Found:", len(ghost_search), "| Expected: 0")
    print("Test 2.1 (Ghost Keyword) - Contains 'magic':", contains_keyword("magic", lone_wolf), "| Expected: False")
    
    # Test 2.2: Target at Maximum Depth

    print("Test 2.2 (Deepest Target) - Contains 'Level 10':", contains_keyword("Level 10", head), "| Expected: True")

    # Test 2.3: Content Truncation Test
    long_text = "A" * 150 # 150个字符的超长评论
    truncated_node = CommentNode(99, "user_C", long_text, "2026-03-18", 0)
    print("Test 2.3 (Truncation) - Content Length:", len(truncated_node.content), "| Expected: 100")

    print("\n=== 3. Deletion Edge Cases ===")
    
    # Test 3.1: Invalid Deletion (Deleting Non-existent ID)
    del_root = CommentNode(100, "user_A", "Root", "time", 0)
    del_reply1 = CommentNode(101, "user_B", "Reply 1", "time", 0)
    del_reply2 = CommentNode(102, "user_C", "Reply 2", "time", 0)
    del_root.add_reply(del_reply1)
    del_root.add_reply(del_reply2)

    # Test 3.1: Invalid Deletion (Deleting Non-existent ID)
    tree_after_invalid_del = delete_comment(999, del_root)
    print("Test 3.1 (Invalid ID) - Replies count after deletion:", len(tree_after_invalid_del.replies), "| Expected: 2")

    # Test 3.2: Deleting an Intermediate Node
    tree_after_valid_del = delete_comment(101, del_root)
    print("Test 3.2 (Intermediate Node) - Replies count after deleting ID 101:", len(tree_after_valid_del.replies), "| Expected: 1")
    print("Test 3.2 (Intermediate Node) - Remaining Reply ID:", tree_after_valid_del.replies[0].comment_id, "| Expected: 102")

    # Test 3.3: Deleting the Root Node
    tree_after_root_del = delete_comment(100, del_root)
    print("Test 3.3 (Root Node) - Tree is None:", tree_after_root_del is None, "| Expected: True")

# Run the edge case tests
if __name__ == "__main__":
    run_edge_case_tests()