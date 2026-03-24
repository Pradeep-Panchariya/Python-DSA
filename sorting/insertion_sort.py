"""
@author : Pradeep Panchariya
"""

"""
Insertion Sort
The Logic: Repeatedly step through the list, compare all the previous element till i and swap them if they are in the wrong order.
Time Complexity: O(n^2) in worst and average case, O(n) in best case (already sorted)
Space Complexity: O(1) - In Place Sort
When to use: Not recommended for large datasets due to poor performance. Useful for educational purposes or small arrays.
"""

from typing import List

class InsertionSort:

    @staticmethod
    def insertion_sort(arr: List[int]) -> List[int]:
        """
        Sorts the array using insertion sort algorithm.
        
        Args:
            arr: List of unsorted integers
            
        Returns:
            The sorted list in ascending order
        """
        if not arr:
            return arr

        for i in range(1,len(arr)):
            for j in range(i,0,-1):
                if arr[j]<arr[j-1]:
                    arr[j-1],arr[j] = arr[j],arr[j-1]
                else:
                    break
        return arr
        


# Test cases
print("Test 1 - Unsorted array:", InsertionSort.insertion_sort([9, 8, 7, 6, 5, 4, 3, 2, 1]))  # Expected: [1, 2, 3, 4, 5, 6, 7, 8, 9]
print("Test 2 - Already sorted:", InsertionSort.insertion_sort([1, 2, 3, 4, 5]))  # Expected: [1, 2, 3, 4, 5]
print("Test 3 - Reverse sorted:", InsertionSort.insertion_sort([5, 4, 3, 2, 1]))  # Expected: [1, 2, 3, 4, 5]
print("Test 4 - Single element:", InsertionSort.insertion_sort([42]))  # Expected: [42]
print("Test 5 - Empty array:", InsertionSort.insertion_sort([]))  # Expected: []