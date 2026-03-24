"""
@author : Pradeep Panchariya
"""

"""
Bubble Sort
The Logic: Repeatedly step through the list, compare adjacent elements and swap them if they are in the wrong order.
Each pass moves the largest element to the end.
Time Complexity: O(n^2) in worst and average case, O(n) in best case (already sorted)
Space Complexity: O(1) - In Place Sort
When to use: Not recommended for large datasets due to poor performance. Useful for educational purposes or small arrays.
"""

from typing import List

class BubbleSort:

    @staticmethod
    def bubble_sort(arr: List[int]) -> List[int]:
        """
        Sorts the array using bubble sort algorithm.
        
        Args:
            arr: List of unsorted integers
            
        Returns:
            The sorted list in ascending order
        """
        if not arr:
            return arr
        
        n = len(arr)
        for i in range(n):
            # Flag to optimize: if no swaps in a pass, array is sorted
            swapped = False
            for j in range(1, n - i):
                if arr[j] < arr[j - 1]:
                    # Swap elements
                    arr[j], arr[j - 1] = arr[j - 1], arr[j]
                    swapped = True
            # If no swaps occurred, array is already sorted
            if not swapped:
                break
        return arr


# Test cases
print("Test 1 - Unsorted array:", BubbleSort.bubble_sort([9, 8, 7, 6, 5, 4, 3, 2, 1]))  # Expected: [1, 2, 3, 4, 5, 6, 7, 8, 9]
print("Test 2 - Already sorted:", BubbleSort.bubble_sort([1, 2, 3, 4, 5]))  # Expected: [1, 2, 3, 4, 5]
print("Test 3 - Reverse sorted:", BubbleSort.bubble_sort([5, 4, 3, 2, 1]))  # Expected: [1, 2, 3, 4, 5]
print("Test 4 - Single element:", BubbleSort.bubble_sort([42]))  # Expected: [42]
print("Test 5 - Empty array:", BubbleSort.bubble_sort([]))  # Expected: []