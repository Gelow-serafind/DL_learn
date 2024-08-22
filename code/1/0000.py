import torch
import numpy

A = torch.tensor([[2,3,4],[1,2,3]])
x = torch.tensor([1,2,3])

Ax = torch.matmul(A,x)
print(Ax)