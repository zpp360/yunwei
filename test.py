#codeing=utf-8
import operator as op

package_name = 'Python-3.6.5.tgz'
version = str(input("请输入您想安装的python脚本(2.7/3.6)"))
if version=='2.7':
    url = 'https://www.python.org/ftp/python/2.7.15/Python-2.7.15.tgz'
elif version == '3.6':
    url = 'https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tgz'
else:
    print('您输入的版本号有误')


print(version)