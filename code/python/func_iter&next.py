# 创建一个可迭代对象（列表）
my_list = [1, 2, 3, 4, 5]

# 使用 iter 函数创建一个迭代器
my_iterator = iter(my_list)

# 使用 next 函数获取迭代器中的下一个项目
print(next(my_iterator))  # 输出: 1
print(next(my_iterator))  # 输出: 2
print(next(my_iterator))  # 输出: 3
print(next(my_iterator))  # 输出: 4
print(next(my_iterator))  # 输出: 5
# 再调用 next(my_iterator) 会引发 StopIteration 异常