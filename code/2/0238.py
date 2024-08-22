import torch

# 定义矩阵 A 和向量 x
A = torch.tensor([[1, 2, 3], [4, 5, 6]])
x = torch.tensor([1, 2, 3])

print(A)
print(x)

# 计算矩阵-向量积
Ax = torch.matmul(A, x)
print(Ax)  # 输出 tensor([14, 32])