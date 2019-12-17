import numpy as np

a = np.random.rand(3, 3)
a = a - a[1][1]
print(a)
x, y = a.nonzero()
print(x)
print(y)

b = a[x][y] + 10
a = b - 10

print(a)