import torch

X1 = torch.tensor([[0,9,0,9],
                  [0,-2,0,0]])

Y1 = torch.tensor([[0,1],
                   [2,3],
                   [3,1],
                   [2,9]])

print(X1@Y1)