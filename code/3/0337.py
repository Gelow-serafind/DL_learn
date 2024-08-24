import random
import torch
from d2l import torch as d2l
from torch.utils import data
from torch import nn

#生成数据与上一节类似
def synthetic_data(w, b, num_examples): 
    """生成y=Xw+b+噪声"""
    X = torch.normal(0, 1, (num_examples, len(w)))
    print("X=",X.shape)
    y = torch.matmul(X, w) + b
    # print("\ny=",y)
    y += torch.normal(0, 0.01, y.shape)
    # print("\ny=",y)
    return X, y.reshape((-1, 1))

def load_array(data_arrays, batch_size, is_train=True): #@save
    """构造一个PyTorch数据迭代器"""
    dataset = data.TensorDataset(*data_arrays)
    return data.DataLoader(dataset, batch_size, shuffle=is_train)

true_w = torch.tensor([2, -3.4])
true_b = 4.2
features, labels = synthetic_data(true_w, true_b, 10000)

batch_size = 1000
data_iter = load_array((features, labels), batch_size)

net = nn.Sequential(nn.Linear(2, 1))

net[0].weight.data.normal_(0, 0.01)
net[0].bias.data.fill_(0)


# loss = nn.HuberLoss()
loss = nn.MSELoss()

trainer = torch.optim.SGD(net.parameters(), lr=0.03)


num_epochs = 10
for epoch in range(num_epochs):
    for X, y in data_iter:
        l = loss(net(X) ,y)
        trainer.zero_grad()
        l.backward()
        trainer.step()
    l = loss(net(features), labels)
    print(f'epoch {epoch + 1}, loss {l:f}')


print("Weight:\n", net[0].weight)
print("Bias:\n", net[0].bias)

