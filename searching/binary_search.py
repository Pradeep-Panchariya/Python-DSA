"""
Binary Search (The Gold Standard)
The Logic: Look at the middle. Discard the half where the target cannot possibly exist. Repeat.
Time Complexity: O(\log n)
Space Complexity: O(1)
When to use: 99% of your sorted array searching. It is perfectly balanced and predictable.

"""


class BinarySearch:
    """Utility class providing binary search on a sorted sequence."""

    @staticmethod
    def binary_search(sorted_array, target):
        """
        Performs a binary search to find the target value index in a sorted array.

        Args:
            sorted_array: List of sorted elements to search through
            target: The value to search for

        Returns:
            The index of the target if found, otherwise -1
        """
        left, right = 0, len(sorted_array) - 1
        while left <= right:
            mid = (left + right) // 2
            if sorted_array[mid] == target:
                return mid
            elif sorted_array[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1 
    
# Example usage and test cases for sorted arrays
print("Test 1 - Found in middle:", BinarySearch.binary_search([1, 2, 3, 4, 5, 6], 2))  # Expected: 1
print("Test 2 - First element:", BinarySearch.binary_search([1, 2, 3, 4, 5, 6], 1))  # Expected: 0
print("Test 3 - Last element:", BinarySearch.binary_search([1, 2, 3, 4, 5, 6], 6))  # Expected: 5
print("Test 4 - Not present:", BinarySearch.binary_search([1, 2, 3, 4, 5, 6], 7))  # Expected: -1
print("Test 5 - Empty list:", BinarySearch.binary_search([], 3))  # Expected: -1