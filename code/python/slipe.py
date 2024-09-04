import torch
import numpy as np

y = torch.tensor([0, 3])
y_hat = torch.tensor([[0.1, 0.3, 0.6, 0.8], [0.3, 0.2, 0.5, 0.9]])
# print(y_hat[[0, 1], y])
print(y_hat[[0, 1], [0, 3]])



m = np.array([[1, 2, 3], 
              [4, 5, 6], 
              [7, 8, 9]])
print(m[1])
print(m[1, 2])             # 输出第二行第三列的元素：6
print(m[[0, 1], [0, 0]])  # 输出第0行第0列和第1行第0列的元素：[1, 4]
