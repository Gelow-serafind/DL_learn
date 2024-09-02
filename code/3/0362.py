import torch

def softmax(X):
    X_exp = torch.exp(X)
    partition = X_exp.sum(1,keepdim=True)
    return X_exp / partition

# X = torch.normal(0, 1, (1, 7))
X = torch.tensor([[9,1,2,3,4]])
print("X= ",X)
X_prob = softmax(X)
print("X_prob= ",X_prob, X_prob.sum(1))
