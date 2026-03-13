class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

# ---------------------------------------------------------
# Part A: Recent Activity Stack (LIFO)
# ---------------------------------------------------------
class ActivityStack:
    def __init__(self):
        self.top = None
        self._size = 0

    def push(self, activity):
        new_node = Node(activity)
        new_node.next = self.top
        self.top = new_node
        self._size += 1

    def pop(self):
        if self.is_empty():
            return None
        temp_node = self.top
        activity_data = temp_node.data
        self.top = self.top.next
        self._size -= 1
        return activity_data

    def peek(self):
        if self.is_empty():
            return None
        return self.top.data

    def is_empty(self):
        return self.top is None

    def size(self):
        return self._size

    def display_recent(self, n):
        current = self.top
        count = 0
        print(f"--- Top {n} Recent Activities ---")
        while current is not None and count < n:
            print(f"- {current.data}")
            current = current.next
            count += 1

    def undo_last(self, undo_stack):
        """Reverts the most recent action and pushes it to an undo stack."""
        if self.is_empty():
            return None
        last_activity = self.pop()
        undo_stack.push(last_activity)
        return last_activity

# ---------------------------------------------------------
# Part B: Notification Queue (FIFO)
# ---------------------------------------------------------
class NotificationQueue:
    def __init__(self):
        self.front_ptr = None
        self.rear_ptr = None
        self._size = 0

    def enqueue(self, notification):
        new_node = Node(notification)
        if self.is_empty():
            self.front_ptr = new_node
            self.rear_ptr = new_node
        else:
            self.rear_ptr.next = new_node
            self.rear_ptr = new_node
        self._size += 1

    def dequeue(self):
        if self.is_empty():
            return None
        temp_node = self.front_ptr
        notification_data = temp_node.data
        self.front_ptr = self.front_ptr.next
        
        # If the queue becomes empty after dequeue, update rear_ptr
        if self.front_ptr is None:
            self.rear_ptr = None
            
        self._size -= 1
        return notification_data

    def front(self):
        if self.is_empty():
            return None
        return self.front_ptr.data

    def is_empty(self):
        return self.front_ptr is None

    def size(self):
        return self._size

    def display_pending(self):
        current = self.front_ptr
        print("--- Pending Notifications ---")
        while current is not None:
            print(f"- {current.data}")
            current = current.next

    def priority_enqueue(self, notification):
        """Adds an urgent notification directly to the front of the queue."""
        new_node = Node(notification)
        new_node.next = self.front_ptr
        self.front_ptr = new_node
        
        # If the queue was empty, update rear_ptr as well
        if self.rear_ptr is None:
            self.rear_ptr = new_node
            
        self._size += 1

# ---------------------------------------------------------
# Part C: Integrated Feed Processing
# ---------------------------------------------------------
class FeedProcessor:
    def __init__(self):
        self.recent_activities = ActivityStack()
        self.notification_queue = NotificationQueue()
        self.processed_log = NotificationQueue()  # Log uses a queue to maintain chronological order

    def process_incoming(self):
        """Moves oldest notification from queue to recent stack."""
        if not self.notification_queue.is_empty():
            notification = self.notification_queue.dequeue()
            self.recent_activities.push(notification)
            return notification
        return None

    def batch_process(self, k):
        """Processes k oldest notifications."""
        processed = 0
        while processed < k and not self.notification_queue.is_empty():
            self.process_incoming()
            processed += 1
        return processed

    def clear_history(self):
        """Moves all items from recent stack to processed_log."""
        while not self.recent_activities.is_empty():
            activity = self.recent_activities.pop()
            self.processed_log.enqueue(activity)

    def get_stats(self):
        """Returns sizes of all three structures."""
        return {
            "recent_activities_size": self.recent_activities.size(),
            "notification_queue_size": self.notification_queue.size(),
            "processed_log_size": self.processed_log.size()
        }
    
def run_edge_case_tests():
    print("=========================================")
    print("      STARTING EDGE CASE TESTS")
    print("=========================================\n")

    # ---------------------------------------------------------
    # 1. Stack
    # ---------------------------------------------------------
    print("--- 1. ActivityStack Edge Cases ---")
    stack = ActivityStack()
    undo_stack = ActivityStack()
    
    # Test operations on an empty stack
    print(f"Pop on empty stack returns None: {stack.pop() is None}")
    print(f"Peek on empty stack returns None: {stack.peek() is None}")
    print(f"Undo on empty stack returns None: {stack.undo_last(undo_stack) is None}")
    
    stack.push("Like Post")
    stack.pop()
    print(f"Size is 0 after pushing and popping all elements: {stack.size() == 0}")
    print(f"Top pointer is None after popping all elements: {stack.top is None}\n")


    # ---------------------------------------------------------
    # 2. Queue
    # ---------------------------------------------------------
    print("--- 2. NotificationQueue Edge Cases ---")
    queue = NotificationQueue()
    
    # Test operations on an empty queue
    print(f"Dequeue on empty queue returns None: {queue.dequeue() is None}")
    print(f"Front on empty queue returns None: {queue.front() is None}")
    
    # Test priority enqueue on an empty queue
    queue.priority_enqueue("Urgent System Alert")
    print(f"Priority enqueue on empty queue sets both front and rear: {queue.front_ptr is not None and queue.front_ptr == queue.rear_ptr}")
    
    # Test rear pointer state after dequeueing the last element
    queue.dequeue()
    print(f"Rear pointer becomes None after dequeueing the last element: {queue.rear_ptr is None}")
    print(f"Size correctly resets to 0: {queue.size() == 0}\n")


    # ---------------------------------------------------------
    # 3. FeedProcessor
    # ---------------------------------------------------------
    print("--- 3. FeedProcessor Edge Cases ---")
    processor = FeedProcessor()
    
    # Test processing incoming with an empty notification queue
    print(f"Process incoming with empty queue returns None: {processor.process_incoming() is None}")
    
    # Test batch processing when requested count exceeds available items
    processor.notification_queue.enqueue("Notif A")
    processor.notification_queue.enqueue("Notif B")
    actual_processed = processor.batch_process(5)
    print(f"Batch process safely stops early (requested 5, processed {actual_processed}): {actual_processed == 2}")
    
    # Test clearing empty activity history
    empty_processor = FeedProcessor()
    try:
        empty_processor.clear_history()
        cleared_safely = True
    except Exception:
        cleared_safely = False
    print(f"Clear history on empty stack executes safely without crashing: {cleared_safely}")
    print(f"Processed log size remains 0: {empty_processor.processed_log.size() == 0}\n")

    print("=========================================")
    print("      ALL TESTS COMPLETED")
    print("=========================================")

# Run Tests
if __name__ == "__main__":
    run_edge_case_tests()