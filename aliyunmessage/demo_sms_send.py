# -*- coding: utf-8 -*-
import sys
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkdysmsapi.request.v20170525 import QuerySendDetailsRequest
from aliyunsdkcore.client import AcsClient
import uuid
from aliyunsdkcore.profile import region_provider
from aliyunsdkcore.http import method_type as MT
from aliyunsdkcore.http import format_type as FT
import const
import subprocess
import re
import logging
"""
短信业务调用接口示例，版本号：v20170525

Created on 2017-06-12

"""

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='ping.log', level=logging.DEBUG, format=LOG_FORMAT)

try:
    reload(sys)
    sys.setdefaultencoding('utf8')
except NameError:
    pass
except Exception as err:
    raise err

# 注意：不要更改
REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"

acs_client = AcsClient(const.ACCESS_KEY_ID, const.ACCESS_KEY_SECRET, REGION)
region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)

def send_sms(business_id, phone_numbers, sign_name, template_code, template_param=None):
    smsRequest = SendSmsRequest.SendSmsRequest()
    # 申请的短信模板编码,必填
    smsRequest.set_TemplateCode(template_code)

    # 短信模板变量参数
    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)

    # 设置业务请求流水号，必填。
    smsRequest.set_OutId(business_id)

    # 短信签名
    smsRequest.set_SignName(sign_name)
	
    # 数据提交方式
	# smsRequest.set_method(MT.POST)
	
	# 数据提交格式
    # smsRequest.set_accept_format(FT.JSON)
	
    # 短信发送的号码列表，必填。
    smsRequest.set_PhoneNumbers(phone_numbers)

    # 调用短信发送接口，返回json
    smsResponse = acs_client.do_action_with_exception(smsRequest)

    # TODO 业务处理

    return smsResponse

def get_ping_result(ip_address):
    p = subprocess.Popen(["ping.exe", ip_address], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, shell=True)
    out = p.stdout.read().decode('gbk')
    logging.info(out)

    reg_receive = ' \d received'
    match_receive = re.search(reg_receive, out)
    receive_count = -1

    if match_receive:
        receive_count = int(match_receive.group()[1:2])
        print(receive_count)

    if receive_count > 0:  # 接受到的反馈大于0，表示网络通
        reg_lose_cout     = ' \d% packet loss'

        match_lose_count = re.search(reg_lose_cout, out)
        lose_count = int(match_lose_count.group()[1:2])
        logging.info('丢失数量：{0}'.format(lose_count))
        return lose_count
    else:
        logging.info('网络不通，目标服务器不可达！')
        return 9999
def send_message():
    __business_id = uuid.uuid1()
    # print(__business_id)
    msg = "nginx服务器网络出现波动···"
    params = "{\"msg\":\"" + msg + "\"}";
    # params = u'{"name":"wqb","code":"12345678","address":"bz","phone":"13000000000"}'
    print(send_sms(__business_id, "17852824020", "老干部APP", "SMS_126461369", params))

if __name__ == '__main__':
    ping_result = get_ping_result('106.75.94.62')
    print(ping_result)
    if (ping_result > 0):
        logging.info("出现丢包···发送短信")
        send_message()


    
    

