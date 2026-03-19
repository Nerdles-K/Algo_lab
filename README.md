**Team Members:** Xu Ziyang, Yuen Kin Ning, Wang Lingyu

**Assigned Exercises:** Xu Ziyang: Ex 1, Yuen Kin Ning: Ex 2, Wang Lingyu: Ex 3

**Brief description of each solution:**

**Ex1:** 

All functions use Depth-First Search (DFS) to recursively traverse the nested tree structure of comment threads, running in O(n) time with O(d) stack space, where n is the total number of comments and d is the maximum nesting depth.

**Ex2:**

 All functions recursively split the array in half and combine results, running in O(n) or O(n log n) time with O(log n) stack space.

**Ex3:** 
 All functions demonstrate conversion from recursion to iteration. flatten_recursive uses DFS recursion, O(n) time, O(d) space. flatten _iterative uses an explicit stack with state machine, O(n) time, O(n) space in worst case. count_comments_tail simulates tail recursion with an accumulator and a linked list of pending nodes, O(n) time, O(n) space. count_comments_loop uses an explicit stack for DFS, O(n) time, O(n) space.


**Complexity analysis summary:**

**Ex1: 		Time complexity 	Space complexity** 

display_thread 	O(n) 				O(d) 

count_total_comments 	O(n) 			O(d) 

total_likes 		O(n) 				O(d) 

find_deepest_reply O(n) 				O(d) 

search_by_user 	O(n) 				O(d) 

contains_keyword	 O(n) 				O(d) 

delete_comment 	O(n) 				O(d)

**Ex2:                              Time complexity  Space complexity**
     max_engagement               O(n)             O(log n)  
     sum_engagement               O(n)             O(log n)  
     average_engagement           O(n)             O(log n)  
     count_above_threshold        O(n)             O(log n)    
     merge_sort_by_engagement     O(n log n)       O(n)   
     find_peak_hour               O(log n)         O(log n)      
     
**Ex3: 		Time complexity       Space complexity**
flatten_recursive       O(n)        O(d)

flatten_iterative       O(n)        O(n)

count_comments_tail     O(n)        O(n)

count_comments_lоор     O(n)        O(n)
