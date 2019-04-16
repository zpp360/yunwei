# coding = utf-8

import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


browser = webdriver.Firefox(executable_path="./geckodriver.exe")
browser.get("https://www.shuhengcare.com")

 #用户名 密码
username = browser.find_element_by_name('loginname')
username.send_keys('shuheng')
password = browser.find_element_by_name('password')
password.send_keys('sh123456!@#QWE')
password.send_keys(Keys.RETURN)
time.sleep(3)
browser.find_element_by_id('lm93').click()
browser.find_element_by_id('z94').click()

time.sleep(5)
assert "baidu" in browser.title
browser.close()
browser.quit()