import heapq
import random
import time
from collections import defaultdict

class HeapEntry:
    """represents a single social media post stored in the heap"""
    def __init__(self, post_id, likes, timestamp):
        self.post_id   = post_id
        self.likes     = likes
        self.timestamp = timestamp

    def __repr__(self):
        return f"HeapEntry(post_id={self.post_id}, likes={self.likes}, timestamp={self.timestamp})"


class TrendingHeap:
    """
    max-heap to track the most-liked posts in real time.

    internally we use python's heapq (which is a min-heap), so we store
    likes as negative values to simulate a max-heap.

    heap entries: (-likes, post_id, timestamp, is_valid[])
    post_index  : dict mapping post_id → index in the heap array (for O(log n) update)

    since python's heapq does not support O(log n) arbitrary updates,
    we use a "lazy deletion" pattern:
      - on update_likes(), we push a new entry and mark the old one as deleted
      - deleted entries are skipped during pop_max() and get_top_k()
    """

    def __init__(self):
        self._heap    = []          
        self._tracker = {}          
        self._size    = 0           


    def push(self, post_id, likes, timestamp):
        """insert a new post into the heap"""
        if post_id in self._tracker:
            self._tracker[post_id][0] = False
            self._size -= 1

        flag = [True]               
        self._tracker[post_id] = flag
        heapq.heappush(self._heap, (-likes, post_id, timestamp, flag))
        self._size += 1

    def pop_max(self):
        """remove and return the post with the highest likes"""
        while self._heap:
            neg_likes, post_id, timestamp, flag = heapq.heappop(self._heap)
            if flag[0]:             
                del self._tracker[post_id]
                self._size -= 1
                return HeapEntry(post_id, -neg_likes, timestamp)
        return None                 
    
    def peek_max(self):
        """read the most-liked post without removing it"""
        while self._heap:
            neg_likes, post_id, timestamp, flag = self._heap[0]
            if flag[0]:
                return HeapEntry(post_id, -neg_likes, timestamp)
            heapq.heappop(self._heap)   
        return None

    def get_top_k(self, k):
        """
        return the top-k posts (by likes) without modifying the original heap.
        strategy: pop from a temporary copy of the heap, then discard the copy.
        time complexity: O(k log n)
        """
        results    = []
        temp_heap  = list(self._heap)   
        count      = 0

        while temp_heap and count < k:
            neg_likes, post_id, timestamp, flag = heapq.heappop(temp_heap)
            if flag[0]:                 
                results.append(HeapEntry(post_id, -neg_likes, timestamp))
                count += 1

        return results

    def update_likes(self, post_id, new_likes, timestamp):
        """
        update the like count for an existing post and reposition it in the heap.
        uses lazy deletion: invalidate the old entry, push a new one.
        """
        if post_id not in self._tracker:
            return                      

        self._tracker[post_id][0] = False
        self._size -= 1

        new_flag = [True]
        self._tracker[post_id] = new_flag
        heapq.heappush(self._heap, (-new_likes, post_id, timestamp, new_flag))
        self._size += 1

    def size(self):
        """return the number of active (non-deleted) posts"""
        return self._size

    def is_valid_heap(self):
        """
        verify the max-heap property:
        every parent must have a higher (or equal) priority than its children.
        we check raw heap entries (including lazily-deleted ones) against python's
        min-heap ordering on (-likes, post_id).
        """
        h = self._heap
        for i in range(len(h)):
            left  = 2 * i + 1
            right = 2 * i + 2
            if left  < len(h) and h[i][0] > h[left][0]:
                return False
            if right < len(h) and h[i][0] > h[right][0]:
                return False
        return True

    def get_height(self):
        """height = number of levels in the complete binary tree"""
        n = len(self._heap)
        if n == 0:
            return 0
        height = 0
        while (1 << height) - 1 < n:   
            height += 1
        return height

    def get_level_order(self):
        """
        return heap entries grouped by level (includes lazy-deleted entries).
        level 0 = root, level 1 = up to 2 nodes, level k = up to 2^k nodes.
        """
        h      = self._heap
        n      = len(h)
        result = []
        level  = 0
        start  = 0
        while start < n:
            end           = min(start + (1 << level), n)   
            level_entries = [
                HeapEntry(pid, -nl, ts)
                for nl, pid, ts, flag in h[start:end]
            ]
            result.append(level_entries)
            start += (1 << level)
            level += 1
        return result

    @staticmethod
    def simulate_trending_feed():
        """
        simulate a real-time trending feed:
          phase 1 — seed 100 posts with random likes (0–1000)
          phase 2 — apply 10,000 like updates with random values (0–10000)
          every 1,000 updates, print a snapshot of the top-5 trending posts.
          at the end, report the average time per update operation.
        """
        h = TrendingHeap()

        for post_id in range(1, 101):
            likes     = random.randint(0, 1000)
            timestamp = int(time.time())
            h.push(post_id, likes, timestamp)

        total_time = 0.0

        for update in range(1, 10_001):
            post_id   = random.randint(1, 100)
            new_likes = random.randint(0, 10_000)

            t_start    = time.perf_counter()
            h.update_likes(post_id, new_likes, int(time.time()))
            total_time += time.perf_counter() - t_start

            if update % 1_000 == 0:
                top5 = h.get_top_k(5)
                print(f"\nafter {update:,} updates — top 5 trending posts:")
                for rank, entry in enumerate(top5, start=1):
                    print(f"  #{rank}  post_id={entry.post_id:<4}  likes={entry.likes:,}")

        avg_ms = (total_time / 10_000) * 1_000
        print(f"\naverage time per update_likes: {avg_ms:.4f} ms")
        print(f"heap is valid: {h.is_valid_heap()}")
        print(f"heap height  : {h.get_height()}")
        print(f"active posts : {h.size()}")

def run_edge_tests():
    passed = 0
    failed = 0

    def check(label, condition):
        nonlocal passed, failed
        status = "PASS" if condition else "FAIL"
        if condition:
            passed += 1
        else:
            failed += 1
        print(f"  [{status}] {label}")

    print("=" * 55)
    print("edge case tests")
    print("=" * 55)

    print("\n[1] pop_max on an empty heap")
    h = TrendingHeap()
    result = h.pop_max()
    check("returns none (no crash)", result is None)
    check("size stays 0", h.size() == 0)

    print("\n[2] peek_max on an empty heap")
    h = TrendingHeap()
    result = h.peek_max()
    check("returns none (no crash)", result is None)

    print("\n[3] get_top_k(1000) when only 50 posts exist")
    h = TrendingHeap()
    for i in range(1, 51):
        h.push(i, random.randint(0, 500), int(time.time()))
    top = h.get_top_k(1000)
    check("returns 50 entries (not 1000)", len(top) == 50)
    check("heap is not destroyed — size still 50", h.size() == 50)
    likes_list = [e.likes for e in top]
    check("results sorted descending by likes", likes_list == sorted(likes_list, reverse=True))

    print("\n[4] update_likes on a post_id that does not exist")
    h = TrendingHeap()
    h.push(1, 100, int(time.time()))
    h.update_likes(999, 9999, int(time.time()))   # post 999 was never inserted
    check("heap size unchanged (still 1)", h.size() == 1)
    check("existing post unaffected", h.peek_max().post_id == 1)

    print("\n" + "=" * 55)
    print(f"results: {passed} passed  |  {failed} failed")
    print("=" * 55)

if __name__ == "__main__":
    run_edge_tests()
    print()
    TrendingHeap.simulate_trending_feed()
