#coding = utf-8
#题目：输入某年某月某日，判断这一天是这一年的第几天？

#程序分析：以3月5日为例，应该先把前两个月的加起来，然后再加上5天即本年的第几天，特殊情况，闰年且输入月份大于2时需考虑多加一天：

year = int(input('year:\n'))
month = int(input('month:\n'))
day = int(input('day:\n'))

months = (0,31,28,31,30,31,30,31,31,30,31,30)

sum = 0

if 0<month<=12:
    for i in range(0,month):
       sum = sum + months[i]
else:
    print("month error")

sum = sum + day

leap = 0
if (year % 400 == 0) or ((year % 4 == 0) and (year % 100 != 0)):
    leap = 1
if (leap == 1) and (month > 2):
    sum += 1

print('it is the %dth day.' % sum)

