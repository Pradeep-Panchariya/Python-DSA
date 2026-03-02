"""
@author : Pradeep Panchariya
"""

"""
Linear Search (The Brute Force)
The Logic: Start at index 0. Check every single item one by one until you find the target.
Time Complexity: O(n)
Space Complexity: O(1)
L5 Reality: You only use this if the array is tiny, or if sorting the array first would cost more time (O(nlog n)) than just searching it once (O(n)).
"""

class LinearSearch():

    @staticmethod
    def linear_search(array, target):
        """
        Performs a linear search to find the target value in an array.
        
        Args:
            array: List of elements to search through
            target: The value to search for
            
        Returns:
            The index of the target if found, otherwise -1
        """
        for index, val in enumerate(array):
            if val == target:
                return index 
        return -1 
    

# Test cases with unsorted array
print("Test 1 - Element exists:", LinearSearch.linear_search([5, 1, 6, 3, 9], 3))  # Expected: 3
print("Test 2 - Element at start:", LinearSearch.linear_search([5, 1, 6, 3, 9], 5))  # Expected: 0
print("Test 3 - Element at end:", LinearSearch.linear_search([5, 1, 6, 3, 9], 9))  # Expected: 4
print("Test 4 - Element not found:", LinearSearch.linear_search([5, 1, 6, 3, 9], 10))  # Expected: -1
print("Test 5 - Empty array:", LinearSearch.linear_search([], 5))  # Expected: -1
