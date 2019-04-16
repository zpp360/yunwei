# coding = utf-8
# fabric中，任务默认都是串行的，可以使用修饰符@parallel修饰任务，使其并行
from fabric.api import *
import time

env.user = 'root'
env.hosts = ['106.75.94.62','117.50.30.45']
env.password = 'sh123456!@#QWE'

tomcat_home = "/usr/tomcat/apache-tomcat-8.5.28/"

def restart():
    time.sleep(20)
    with cd(tomcat_home + "bin"):
        run("sh shutdown.sh")
        time.sleep(20)
    with cd(tomcat_home + "webapps/SHYL"):
        run("pwd")
        sudo("ls -l")

        # run("git add .")
        # run("git commit -m 'fabric提交测试'")
        # run("git push")
        # run("git diff master")
        # run("git remote -v")
        # run('git fetch --all')
        # run("git reset --hard origin/master")
        run('git pull')
    time.sleep(5)

    run(tomcat_home + "bin/startup.sh",pty=False)

def no_restart():
    with cd(tomcat_home + "webapps/SHYL"):
        run("pwd")
        sudo("ls -l")

        # run("git add .")
        #         # run("git commit -m 'fabric提交测试'")
        #         # run("git push")
        #         # run("git diff master")
        #         # run("git remote -v")
        # run('git fetch --all')
        # run("git reset --hard origin/master")
        run('git pull')
    time.sleep(5)




