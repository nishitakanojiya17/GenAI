import numpy as np

scores = np.array([78, 85, 92, 68, 88, 74, 96])

print("Scores:", scores)
print("Mean:", np.mean(scores))
print("Median:", np.median(scores))
print("Min:", np.min(scores))
print("Max:", np.max(scores))
print("Standard deviation:", np.std(scores))
print("Variance:", np.var(scores))

# Sorting
print("Sorted scores:", np.sort(scores))
