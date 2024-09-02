import torch

num_input  = 5
num_outputs = 10

w = torch.normal(0, 0.01, size=(num_input,num_outputs), requires_grad=True)
b = torch.zeros(num_outputs, requires_grad = True)


def softmax(X):
    X_exp = torch.exp(X)
    partition = X_exp.sum(1,keepdim=True)
    return X_exp / partition

def net(X):
    return softmax(torch.matmul(X.reshape((-1, w.shape[0])), w) + b)


print(w.shape)
X = torch.tensor([[9.,1.,2.,3.,4.]])
print("X= ",X)
print("net= ",net(X))