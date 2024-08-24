# nn是神经网络的缩写
from torch import nn
import torch


net = nn.Sequential(nn.Linear(2, 10))


net[0].weight.data.normal_(0, 0.01)
net[0].bias.data.fill_(0)

#以下为测试部分
input = torch.tensor([[2.,2.]])
output = net(input)

print(output)


