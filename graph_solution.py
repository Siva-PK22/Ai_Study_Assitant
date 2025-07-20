from typing import List

class Solution:
    def minCost(self, n: int, edges: List[List[int]], k: int) -> int:
        """
        Find the minimum possible value of the maximum cost among all components
        after removing edges to have at most k connected components.
        
        Args:
            n: Number of nodes (0 to n-1)
            edges: List of [u, v, weight] representing undirected edges
            k: Maximum number of connected components allowed
            
        Returns:
            Minimum possible maximum cost among all components
        """
        # Edge case: if k >= n, we can remove all edges
        if k >= n:
            return 0
        
        # Sort edges by weight in ascending order
        edges.sort(key=lambda x: x[2])
        
        # Binary search on the answer
        def canAchieve(maxCost):
            """Check if we can achieve at most k components with max cost <= maxCost"""
            # Union-Find to track components
            parent = list(range(n))
            rank = [0] * n
            components = n
            
            def find(x):
                if parent[x] != x:
                    parent[x] = find(parent[x])
                return parent[x]
            
            def union(x, y):
                nonlocal components
                px, py = find(x), find(y)
                if px == py:
                    return False
                
                if rank[px] < rank[py]:
                    px, py = py, px
                parent[py] = px
                if rank[px] == rank[py]:
                    rank[px] += 1
                components -= 1
                return True
            
            # Add edges with weight <= maxCost
            for u, v, w in edges:
                if w <= maxCost:
                    union(u, v)
                    if components <= k:
                        return True
            
            return components <= k
        
        # Binary search on the maximum cost
        left, right = 0, max(edge[2] for edge in edges) if edges else 0
        result = right
        
        while left <= right:
            mid = (left + right) // 2
            if canAchieve(mid):
                result = mid
                right = mid - 1
            else:
                left = mid + 1
        
        return result


# Test cases
if __name__ == "__main__":
    solution = Solution()
    
    # Example 1
    n1 = 5
    edges1 = [[0,1,4],[1,2,3],[1,3,2],[3,4,6]]
    k1 = 2
    result1 = solution.minCost(n1, edges1, k1)
    print(f"Example 1:")
    print(f"n = {n1}, edges = {edges1}, k = {k1}")
    print(f"Output: {result1}")
    print()
    
    # Additional test cases
    # Test case 2: k >= n (can remove all edges)
    n2 = 3
    edges2 = [[0,1,5],[1,2,10]]
    k2 = 3
    result2 = solution.minCost(n2, edges2, k2)
    print(f"Example 2:")
    print(f"n = {n2}, edges = {edges2}, k = {k2}")
    print(f"Output: {result2}")
    print()
    
    # Test case 3: Need to keep some edges
    n3 = 4
    edges3 = [[0,1,1],[1,2,2],[2,3,3],[0,3,4]]
    k3 = 2
    result3 = solution.minCost(n3, edges3, k3)
    print(f"Example 3:")
    print(f"n = {n3}, edges = {edges3}, k = {k3}")
    print(f"Output: {result3}")
