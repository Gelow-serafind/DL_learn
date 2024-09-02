if __name__ == '__main__':
    import torch
    import torchvision
    from torch.utils import data
    from torchvision import transforms
    from d2l import torch as d2l
    import multiprocessing

    multiprocessing.freeze_support()

    def get_dataloader_workers(): #@save
        """使用4个进程来读取数据"""
        return 4

    def load_data_fashion_mnist(batch_size, resize=None):
        """下载Fashion-MNIST数据集并加载到内存中"""

        # 定义图像转换，首先将图像转换为张量
        transformations = [transforms.ToTensor()]

        # 如果指定了图像大小，则添加调整大小的转换
        if resize:
            transformations.insert(0, transforms.Resize(resize))

        # 将所有转换组合成一个复合转换
        transform = transforms.Compose(transformations)

        # 加载训练集
        train_dataset = torchvision.datasets.FashionMNIST(root="../data", train=True, transform=transform, download=True)

        # 加载测试集
        test_dataset = torchvision.datasets.FashionMNIST(root="../data", train=False, transform=transform, download=True)

        # 使用DataLoader包装数据集，用于高效数据加载
        # train_loader = data.DataLoader(train_dataset, batch_size, shuffle=True, num_workers=get_dataloader_workers())
        train_loader = data.DataLoader(train_dataset, batch_size, shuffle=True, num_workers=4)

        # test_loader = data.DataLoader(test_dataset, batch_size, shuffle=False, num_workers=get_dataloader_workers())
        test_loader = data.DataLoader(test_dataset, batch_size, shuffle=False, num_workers=4)

        # 返回训练和测试数据加载器
        return train_loader, test_loader

    train_iter, test_iter = load_data_fashion_mnist(32, resize=64)
    for X, y in train_iter:
        print(X.shape, X.dtype, y.shape, y.dtype)
        break
