import numpy as np

A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

print("Matrix A:\n", A)
print("Matrix B:\n", B)

print("Matrix addition:\n", A + B)
print("Matrix subtraction:\n", A - B)
print("Matrix multiplication:\n", A @ B)
print("Element-wise multiplication:\n", A * B)

# Transpose
print("Transpose of A:\n", A.T)

# Identity matrix
I = np.eye(3)
print("Identity matrix:\n", I)
