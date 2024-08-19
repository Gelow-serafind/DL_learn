import torch

A = torch.tensor((1,2))
print(A)
print(A.shape)
X = torch.arange(12)
print(X)
print(X.shape)

X = X.reshape(4,3)
print(X)

print("----------------")
a = torch.arange(3).reshape((3, 1))
b = torch.arange(2).reshape((1, 2))
print(a)
print(b)
print(a+b)