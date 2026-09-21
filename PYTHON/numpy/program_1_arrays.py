import numpy as np

# Create a 1D array
arr = np.array([10, 20, 30, 40, 50])
print("1D Array:", arr)

# Create a 2D array
matrix = np.array([[1, 2, 3], [4, 5, 6]])
print("2D Array:\n", matrix)

# Accessing elements
print("First element:", arr[0])
print("Row 2:", matrix[1])

# Slicing
print("Slice arr[1:4]:", arr[1:4])
print("Column 1:", matrix[:, 1])

# Reshaping
reshaped = arr.reshape(5, 1)
print("Reshaped array:\n", reshaped)

# Basic operations
print("Array + 5:", arr + 5)
print("Square root:", np.sqrt(arr))
