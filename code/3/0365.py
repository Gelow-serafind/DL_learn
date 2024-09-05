import torch
from d2l import torch as d2l

class Accumulator:
    """在n个变量上累加"""
    
    def __init__(self, n):
        # 初始化n个变量为0.0
        self.data = [0.0] * n
    
    def add(self, *args):
        # 对传入的可变参数列表中的每个元素与现有的对应元素相加
        self.data = [a + float(b) for a, b in zip(self.data, args)]
    
    def reset(self):
        # 重置所有累积变量为0.0
        self.data = [0.0] * len(self.data)
    
    def __getitem__(self, idx):
        # 返回第idx个累积变量的值
        return self.data[idx]


def softmax(X):
    X_exp = torch.exp(X)
    partition = X_exp.sum(1,keepdim=True)
    return X_exp / partition

def net(X):
    return softmax(torch.matmul(X.reshape((-1, w.shape[0])), w) + b)

def accuracy(y_hat, y): 
    """计算预测正确的数量"""
    if len(y_hat.shape) > 1 and y_hat.shape[1] > 1:
        y_hat = y_hat.argmax(axis=1)
    cmp = y_hat.type(y.dtype) == y
    return float(cmp.type(y.dtype).sum())

def evaluate_accuracy(net, data_iter): 
    """计算在指定数据集上模型的精度"""
    if isinstance(net, torch.nn.Module):
        net.eval() # 将模型设置为评估模式
    metric = Accumulator(2) # 正确预测数、预测总数
    with torch.no_grad():
        for X, y in data_iter:
            metric.add(accuracy(net(X), y), y.numel())
    return metric[0] / metric[1]


if __name__ == '__main__':

    y = torch.tensor([0, 2]) 
    y_hat = torch.tensor([[0.1, 0.3, 0.6], 
                        [0.3, 0.2, 0.5]]) 

    batch_size = 256
    train_iter, test_iter = d2l.load_data_fashion_mnist(batch_size)

    num_input  = 784
    num_outputs = 10

    w = torch.normal(0, 0.01, size=(num_input,num_outputs), requires_grad=True)
    b = torch.zeros(num_outputs, requires_grad = True)


    # print(accuracy(y_hat,y)/len(y_hat))
    print(evaluate_accuracy(net, test_iter))