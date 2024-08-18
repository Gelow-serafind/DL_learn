import torch

# 定义 x 变量
x = torch.tensor([2.0], requires_grad=True)

# 不分离情况
y = x ** 2
z = y * x
z.backward()
print(f'不分离情况的梯度: {x.grad}')  # 输出 12（对应 3x^2）

# 分离情况
x.grad.zero_()  # 清除先前的梯度
y_const = y.detach()  # 将 y 视为常数
z_new = y_const * x
z_new.backward()
print(f'分离情况的梯度: {x.grad}')  # 输出 4（对应 x^2）
