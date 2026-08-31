"""
@author : Pradeep Panchariya
"""

"""
Merge Sort
The Logic: Iterate through the list; for each position, find the minimum element in the unsorted suffix and swap it into place.
Time Complexity: O(n Log n) worst and average case, O(n^2) best case
Space Complexity: O(n) - In place sort
When to use: Not recommended for large datasets due to poor performance. Useful for educational purposes or small arrays.
"""

from typing import List

class MergeSort:

    @staticmethod
    def merge_sort(arr: List[int]) -> List[int]:
        """
        Sorts the array using merge sort algorithm.

        The algorithm selects the minimum element from the unsorted portion
        and swaps it with the first unsorted element.

        Time Complexity: O(n^2) worst/average, O(n^2) best
        Space Complexity: O(1) in-place

        Args:
            arr: List of unsorted integers

        Returns:
            The sorted list in ascending order
        """



if __name__ == "__main__":
    # Test cases
    print("Test 1 - Unsorted array:", MergeSort.merge_sort([9, 8, 7, 6, 5, 4, 3, 2, 1]))  # Expected: [1, 2, 3, 4, 5, 6, 7, 8, 9]
    print("Test 2 - Already sorted:", MergeSort.merge_sort([1, 2, 3, 4, 5]))  # Expected: [1, 2, 3, 4, 5]
    print("Test 3 - Reverse sorted:", MergeSort.merge_sort([5, 4, 3, 2, 1]))  # Expected: [1, 2, 3, 4, 5]
    print("Test 4 - Single element:", MergeSort.merge_sort([42]))  # Expected: [42]
    print("Test 5 - Empty array:", MergeSort.merge_sort([]))  # Expected: []

