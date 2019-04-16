#coding = utf-8
#输入三个整数x,y,z，请把这三个数由小到大输出。

l = []
for i in range(0,3):
    l.append(input("第%d个数字：" %i))
l.sort()
print(l)