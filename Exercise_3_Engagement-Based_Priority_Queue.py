import time

class Post:
    def __init__(self, post_id, user_id, content, likes=0, comments=0, shares=0):
        self.post_id = post_id
        self.user_id = user_id
        self.content = content
        self.timestamp = int(time.time())
        self.likes = likes
        self.comments = comments
        self.shares = shares
        self.engagement_score = (likes * 1) + (comments * 2) + (shares * 3)
        self.next = None

class PriorityQueue:
    def __init__(self):
        self.head = None
        self.size = 0

    def is_empty(self):
        return self.head is None

    def enqueue(self, postNode):
        if self.is_empty() or self.head.engagement_score < postNode.engagement_score:
            postNode.next = self.head
            self.head = postNode
        else:
            current = self.head
            while current.next is not None and current.next.engagement_score >= postNode.engagement_score:
                current = current.next
            postNode.next = current.next
            current.next = postNode
        self.size += 1

    def dequeue_max(self):
        if self.is_empty():
            return None
        topPost = self.head
        self.head = self.head.next
        self.size -= 1
        return topPost

    def peek_max(self):
        return self.head

    def update_score(self, post_id, new_likes, new_comments, new_shares):
        current = self.head
        prev = None
        
        while current is not None and current.post_id != post_id:
            prev = current
            current = current.next
            
        if current is None:
            return
            
        if prev is None:
            self.head = current.next
        else:
            prev.next = current.next
        self.size -= 1
        
        current.likes = new_likes
        current.comments = new_comments
        current.shares = new_shares
        current.engagement_score = (new_likes * 1) + (new_comments * 2) + (new_shares * 3)
        current.next = None
        
        self.enqueue(current)

if __name__ == "__main__":
    pq = PriorityQueue()
    print("Test 1: Dequeue empty:", pq.dequeue_max())
    
    pq.enqueue(Post(1, 201, "Low", 1, 1, 1))
    pq.enqueue(Post(2, 202, "High", 10, 10, 10))
    print("Test 2: Head ID after high priority enqueue (Expected 2):", pq.peek_max().post_id)
    
    pq.update_score(2, 0, 0, 0)
    print("Test 3: Head ID after score drop (Expected 1):", pq.peek_max().post_id)