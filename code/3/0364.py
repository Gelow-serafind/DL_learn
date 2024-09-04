import torch

y = torch.tensor([0, 3])
y_hat = torch.tensor([[0.1, 0.3, 0.6, 0.8], [0.3, 0.2, 0.5, 0.9]])
print(y_hat[[0, 1], y])

def cross_entropy(y_hat, y):
    return - torch.log(y_hat[range(len(y_hat)), y])

cross_entropy(y_hat, y)

