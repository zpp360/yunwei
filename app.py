#codeing=utf-8
import os
import sys

if os.getuid() == 0:
    pass
else:
    print("当前用户不是root用户，请以root用户执行脚本")
    sys.exit(1)

version = input("请输入您想安装的python脚本(2.7/3.6)")
print(version)
if version == '2.7':
    url = 'https://www.python.org/ftp/python/2.7.15/Python-2.7.15.tgz'
elif version == '3.6':
    url = 'https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tgz'
else:
    print('您输入的版本号有误')
    sys.exit(1)

cmd = "wget " + url
res = os.system(cmd)
if res != 0:
    print("下载源码包失败，请检查网络")
    sys.exit(1)

if version == '2.7':
    package_name = 'Python-2.7.15.tgz'
else:
    package_name = 'Python-3.6.5.tgz'

cmd = 'tar xf ' + package_name

res = os.system(cmd)

if res != 0:
    os.system("rm "+package_name)
    print("解压源码包失败，请重新运行脚本下载源码")
    sys.exit(1)

cmd = 'cd '+package_name[:-4]+' && ./configure --prefix=/usr/local/python && make && make install'
res = os.system(cmd)
if res != 0:
    print('编译python源码失败，请检查是否缺少依赖库')
    sys.exit(1)



