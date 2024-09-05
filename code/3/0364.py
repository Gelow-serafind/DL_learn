import torch
import math

# def cross_entropy(y_hat, y):
#     return - torch.log(y_hat[range(len(y_hat)), y])


def cross_entropy(y_hat, y):
    losses = []  # 创建一个列表来存储每个样本的损失
    for i in range(len(y_hat)):
        correct_prob = y_hat[i][y[i]]
        loss_i = -torch.log(correct_prob)
        losses.append(loss_i)  # 将损失添加到列表
    return torch.tensor(losses)  # 返回所有损失的张量


#模拟的类别
y = torch.tensor([0, 2]) 
#模拟的样本
y_hat = torch.tensor([[0.1, 0.3, 0.6], 
                      [0.3, 0.2, 0.5]]) 
# print(y_hat[[0, 1], y])

print(cross_entropy(y_hat, y))

