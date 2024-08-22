import torch

#----------------非标量对标量求导--------------------
# 定义矩阵 A 和向量 x
if 0:
    A = torch.tensor([[1., 2.], [3., 4.]], requires_grad=True)
    x = torch.tensor([1., 2.], requires_grad=True)

    # 计算矩阵-向量积 y
    y = torch.matmul(A, x)
    print("y=",y)
    # 对 y 的某一个元素求导，比如 y[0]
    y[0].backward()

    # 打印 A 和 x 的梯度
    print(A.grad)  # 对 A 的梯度
    print(x.grad)  # 对 x 的梯度

#----------------非标量对非标量求导------------------
if 1:

    # 定义矩阵 A 和向量 x
    A = torch.tensor([[1., 2.], [3., 4.]], requires_grad=True)
    x = torch.tensor([1., 2.], requires_grad=True)

    # 计算矩阵-向量积 y
    y = torch.matmul(A, x)
    print("y=",y)
    # 创建雅可比矩阵的存储空间
    jacobian = torch.zeros((2, 2))
    print("jacobian_0=\n",jacobian)

    # 逐个计算 y 的每个分量对 x 的导数
    for i in range(2):
        y[i].backward(retain_graph=True)
        jacobian[i] = x.grad
        x.grad.zero_()  # 清空梯度以便计算下一个分量

    print("jacobian=\n",jacobian)
