import random
import torch
from d2l import torch as d2l

#初始化模型的参数
w = torch.normal(0, 0.01, size=(2,1), requires_grad=True)
b = torch.zeros(1, requires_grad=True)

