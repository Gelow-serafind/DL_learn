import torch

def cross_entropy(y_hat, y):
    return - torch.log(y_hat[range(len(y_hat)), y])


y = torch.tensor([0, 2])
y_hat = torch.tensor([[0.1, 0.3, 0.6], [0.3, 0.2, 0.5]])
# print(y_hat[[0, 1], y])

print(cross_entropy(y_hat, y))

