**Team Members:** Xu Ziyang, Yuen Kin Ning, Wang Lingyu

**Assigned Exercises:** Xu Ziyang: Ex 1, Yuen Kin Ning: Ex 2, Wang Lingyu: Ex 3

**Brief description of each solution:**

**Ex1:** 

All functions use Depth-First Search (DFS) to recursively traverse the nested tree structure of comment threads, running in O(n) time with O(d) stack space, where n is the total number of comments and d is the maximum nesting depth.

**Ex2:**

 All functions recursively split the array in half and combine results, running in O(n) or O(n log n) time with O(log n) stack space.

**Ex3:** 



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
