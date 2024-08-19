import torch
x = torch.tensor([16.],requires_grad=True)
y = x*x*x + 3
y.backward()
print(x.grad)