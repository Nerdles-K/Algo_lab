import time

class StoryNode:
    def __init__(self, story_id, user_id, content_preview):
        self.story_id = story_id
        self.user_id = user_id
        self.content_preview = content_preview
        self.timestamp = int(time.time())
        self.views = 0
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None
        self.size = 0

    def add_story(self, node):
        node.next = None
        node.prev = self.tail
        
        if self.tail is not None:
            self.tail.next = node
        else:
            self.head = node
            
        self.tail = node
        
        if self.current is None:
            self.current = node
            
        self.size += 1

    def remove_story(self, story_id):
        node = self.head
        while node is not None:
            if node.story_id == story_id:
                if node.prev is not None:
                    node.prev.next = node.next
                else:
                    self.head = node.next
                
                if node.next is not None:
                    node.next.prev = node.prev
                else:
                    self.tail = node.prev
                
                if self.current == node:
                    if node.next is not None:
                        self.current = node.next
                    else:
                        self.current = node.prev
                
                self.size -= 1
                return True
            node = node.next
        return False

    def move_forward(self):
        if self.current is None or self.current.next is None:
            return None
        self.current = self.current.next
        return self.current

    def move_backward(self):
        if self.current is None or self.current.prev is None:
            return None
        self.current = self.current.prev
        return self.current

    def jump_to(self, story_id):
        node = self.head
        while node is not None:
            if node.story_id == story_id:
                self.current = node
                return True
            node = node.next
        return False

    def insert_after(self, current_id, new_story):
        node = self.head
        while node is not None:
            if node.story_id == current_id:
                new_story.prev = node
                new_story.next = node.next
                if node.next is not None:
                    node.next.prev = new_story
                else:
                    self.tail = new_story
                node.next = new_story
                self.size += 1
                return True
            node = node.next
        return False

    def display_around_current(self, k):
        if self.current is None:
            return []
        
        result = []
        node = self.current
        count = 0
        while node.prev is not None and count < k:
            node = node.prev
            count += 1
            
        steps = 0
        while node is not None and steps <= 2 * k:
            result.append(node.story_id)
            node = node.next
            steps += 1
        return result

    def track_view(self):
        if self.current is not None:
            self.current.views += 1

    def most_viewed(self):
        if self.head is None:
            return None
        best = self.head
        node = self.head.next
        while node is not None:
            if node.views > best.views:
                best = node
            node = node.next
        return best

    def reorder_by_views(self):
        if self.head is None: return
        
        arr = []
        node = self.head
        while node is not None:
            arr.append(node)
            node = node.next
            
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and arr[j].views < key.views:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
            
        self.head = arr[0]
        self.tail = arr[len(arr) - 1]
        for i in range(len(arr)):
            arr[i].prev = arr[i - 1] if i > 0 else None
            arr[i].next = arr[i + 1] if i < len(arr) - 1 else None

if __name__ == "__main__":
    dll = DoublyLinkedList()
    print("Test 1: Remove from empty:", dll.remove_story(1))
    
    dll.add_story(StoryNode(1, 101, "Story A"))
    dll.remove_story(1)
    print("Test 2: Size after removing only node:", dll.size)
    
    dll.add_story(StoryNode(2, 102, "Story B"))
    dll.add_story(StoryNode(3, 103, "Story C"))
    dll.jump_to(3)
    print("Test 3: Move forward at tail:", dll.move_forward())