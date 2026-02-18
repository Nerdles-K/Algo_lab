**Team Members: Yuen Kin Ning, Xu Ziyang**

Assigned Exercises: Yuen Kin Ning: **Ex 1,3**  Xu Ziyang: **Ex 2,4**

**Brief description of each solution:** 

Ex1: Analyzes message sentiment and spam by scanning the string once to calculate character ratios and detect repeating patterns.

Ex2: This implementation utilizes Hash Set operations (Intersection, Difference) to efficiently identify mutual connections and friend-of-friend suggestions.

Ex3: Recommends new items by using cosine similarity math on a user-interest matrix to find profiles with matching tastes.

Ex4: This implementation models a directed social graph using a 2D Boolean Adjacency Matrix.

**Complexity analysis summary:** 

Ex1: 
time complexity: O(n)
space complexity: O(1)

Ex2: 

| Operation          | Time Complexity  |
| ------------------ | ---------------- |
| Intersection       | O(min(M, N))     |
| Difference         | O(M)             |
| Union              | O(M + N)         |
| Jaccard Similarity | O(M + N)         |
| Get Suggestions    | O(N<sup>2</sup>) |
| Space Complexity   | O(M + N)         |

Ex3: 
time complexity: O(U x I)
space complexity: O(U x I)

Ex4: 

| Operation         | Time Complexity  |
| ----------------- | ---------------- |
| Follow / Unfollow | O(1)             |
| Is_Following      | O(1)             |
| Get_Followers     | O(N)             |
| Get_Following     | O(N)             |
| Mutual Follows    | O(N<sup>2</sup>) |
| Influence Score   | O(N)             |
| Space Complexity  | O(N<sup>2</sup>) |



