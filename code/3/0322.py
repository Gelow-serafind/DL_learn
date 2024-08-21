import random
import torch
from d2l import torch as d2l

def synthetic_data(w, b, num_examples): 
    """生成y=Xw+b+噪声"""
    X = torch.normal(0, 1, (num_examples, len(w)))
    print("X=",X.shape)
    y = torch.matmul(X, w) + b
    # print("\ny=",y)
    y += torch.normal(0, 0.01, y.shape)
    # print("\ny=",y)
    return X, y.reshape((-1, 1))

def data_iter(batch_size, features, labels):
    num_examples = len(features)
    indices = list(range(num_examples))
    # 这些样本是随机读取的，没有特定的顺序
    random.shuffle(indices)
    for i in range(0, num_examples, batch_size):
        batch_indices = torch.tensor(
            indices[i: min(i + batch_size, num_examples)])
        yield features[batch_indices], labels[batch_indices]

true_w = torch.tensor([2, -3.4])
true_b = 4.2
features, labels = synthetic_data(true_w, true_b, 1000)

batch_size = 10
for X, y in data_iter(batch_size, features, labels):
    print(X, '\n', y)
    break


