import os
import pandas as pd

# os.makedirs(os.path.join('..', 'File'), exist_ok=True)
data_file = os.path.join(r'C:\Users\12262\OneDrive\#成长资料\0_人生沉淀\1_程序与算法\DeepLearning\pytorch\code\File', 'house_tiny.csv')

with open(data_file, 'w') as f:
    f.write('NumRooms,Alley,Price\n') # 列名
    f.write('NA,Pave,127500\n') # 每行表示一个数据样本
    f.write('2,NA,106000\n')
    f.write('4,NA,178100\n')
    f.write('NA,NA,140000\n')
    print("load success")

data = pd.read_csv(data_file)
print(data)

