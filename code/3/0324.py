import torch

#定义模型
def linreg(X, w, b): #@save
    """线性回归模型"""
    return torch.matmul(X, w) + b