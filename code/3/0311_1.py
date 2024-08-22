#损失函数

import torch
import torch.nn as nn

# 定义真实值和预测值
y_true = torch.tensor([3.0, 5.0, 2.5, 7.0])
y_pred = torch.tensor([2.8, 5.1, 2.3, 6.8])

# 定义均方误差损失函数
mse_loss = nn.MSELoss()

# 计算损失
loss = mse_loss(y_pred, y_true)
print(loss)  # 输出损失值