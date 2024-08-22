import torch
A = torch.arange(4)
B = torch.arange(4)
Dot_AB = torch.sum(A*B)
print(Dot_AB)
DOT = torch.dot(A,B)
print(DOT)