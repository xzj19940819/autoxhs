
# encoding:utf-8
import os
import sys
import json
import requests
import base64
import time
import re


# 保证兼容python2以及python3
IS_PY3 = sys.version_info.major == 3
if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode
    from urllib.parse import quote_plus
else:
    import urllib2
    from urllib import quote_plus
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib2 import URLError
    from urllib import urlencode

    # 防止https证书校验不正确
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


'''
图像主体检测
'''


# 配图像主体识别
# APP_ID = '26488994'
# API_KEY = 'wjlqvbT4ldUqQAR3e45OoGvG'
# SECRET_KEY = 'S6nE3oGzN45Emx92tXa6O84VAKgBxjaI'
# TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'

APP_ID = '26489354'
API_KEY = 'IgwfMAx7fiKeKZXmIHgFHz1Y'
SECRET_KEY = '7TeeG9671KuOpwcdYklMaqfblBDlhd1V'
TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'
G_PHONENUM = 'NULL'
G_PHONETEXT = 'NULL'

def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    if (IS_PY3):
        post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        print(err)
    if (IS_PY3):
        result_str = result_str.decode()


    result = json.loads(result_str)

    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not 'brain_all_scope' in result['scope'].split(' '):
            print ('please ensure has check the  ability')
            exit()
        return result['access_token']
    else:
        print ('please overwrite the correct API_KEY and SECRET_KEY')
        exit()


def vimmy_getbaiduimg():
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/object_detect"
     # 获取access token
    access_token = fetch_token()
    # 二进制方式打开图片文件
    f = open('img/autolottery.png', 'rb')
    img = base64.b64encode(f.read())

    params = {"image":img,"with_face":0}

    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        print (response.json())

def vimmy_getphonesreen():
    os.system('adb shell screencap -p /sdcard/autolottery.png')
    os.system('adb pull /sdcard/autolottery.png ./img')

def vimmy_getbaiduimgtext():
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general"
    # 二进制方式打开图片文件
    f = open('img/autolottery.png', 'rb')
    img = base64.b64encode(f.read())

    params = {"image":img}
      # 获取access token
    access_token = fetch_token()
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        print (response.json())

def adb_click(randomX,randomY):
    cmd = 'adb shell input tap ' + str(randomX) + ' ' + str(randomY)
    os.popen(cmd)
    print('input(%d,%d)',randomX, randomY)

def adb_inputtext(phonenum):
    cmd = 'adb shell input text ' + phonenum
    os.popen(cmd)
    print('input',phonenum)

def vimmy_entryxiaohongshu():
    print('VIMIY自动化脚本：打开小红书\n')
    adb_click(916,1090)
    time.sleep(10)
    print('VIMIY自动化脚本：打开手机登录页面\n')
    adb_click(487,1664)
    time.sleep(5)
    print('VIMIY自动化脚本：清空手机号码\n')
    adb_click(876,630)
    time.sleep(5)
    print('VIMIY自动化脚本：输入手机号码\n')
    adb_inputtext(G_PHONENUM)
    time.sleep(5)
    print('VIMIY自动化脚本：获取验证码\n')
    adb_click(818,797)
    time.sleep(5)

def vimmy_getremotephonenum_login():
    print('VIMIY自动化脚本：登录手机信息获取平台\n')
    request_url = "http://api.d1jiema.com/zc/data.php"
    request_url = request_url + "?code=signIn&user=xzj19940819&password=WangDao"
# headers = {'content-type': 'application/x-www-form-urlencoded'}
    print (request_url)
    response = requests.get(request_url)
    if response:
        # 查看响应状态码
        print (response.status_code)

        # 查看响应头部字符编码
        print (response.encoding)

        # 查看完整url地址
        print (response.url)

        # 查看响应内容，response.text 返回的是Unicode格式的数据
        print(response.text)

        # 获取access token
        access_token = response.text
        return access_token

    return "null"

def vimmy_getremotephonenum_getmoney(access_token):
    print('VIMIY自动化脚本：获取手机信息获取平台余额\n')
    request_url = "http://api.d1jiema.com/zc/data.php?code=leftAmount&token=" + access_token
# headers = {'content-type': 'application/x-www-form-urlencoded'}
    print (request_url)
    response = requests.get(request_url)
    if response:
        # 查看响应状态码
        print (response.status_code)

        # 查看响应头部字符编码
        print (response.encoding)

        # 查看完整url地址
        print (response.url)

        # 查看响应内容，response.text 返回的是Unicode格式的数据
        print(response.text)

def vimmy_getremotephonenum_getphoenum(access_token):
    print('VIMIY自动化脚本：获取手机信息获取手机号码\n')
    request_url = "http://api.d1jiema.com/zc/data.php?code=getPhone&token=" + access_token
# headers = {'content-type': 'application/x-www-form-urlencoded'}
    print (request_url)
    response = requests.get(request_url)
    if response:
        # 查看响应状态码
        print (response.status_code)

        # 查看响应头部字符编码
        print (response.encoding)

        # 查看完整url地址
        print (response.url)

        # 查看响应内容，response.text 返回的是Unicode格式的数据
        print(response.text)

        return response.text
    return "null"

def vimmy_getremotephonenum_getphoetext(access_token,tmp_phonenum):
    print('VIMIY自动化脚本：获取手机信息获取小红书短信\n')
    request_url = "http://api.d1jiema.com/zc/data.php?code=getMsg&token=" + access_token+"&phone=" + tmp_phonenum+ "&keyWord=小红书"
# headers = {'content-type': 'application/x-www-form-urlencoded'}
    print (request_url)
    response = requests.get(request_url)
    if response:
        # 查看响应状态码
        print (response.status_code)

        # 查看响应头部字符编码
        print (response.encoding)

        # 查看完整url地址
        print (response.url)

        # 查看响应内容，response.text 返回的是Unicode格式的数据
        print(response.text)

        return response.text
    return "null"

def vimmy_getremotephonenum_getfinalcode():
    vimmy_token = vimmy_getremotephonenum_login()
    #vimmy_token = 'b3c63bc0d43342d9a3321275310b4564'
    if(vimmy_token.find("null") == -1):
        vimmy_getremotephonenum_getmoney(vimmy_token)
        vimmy_phonenum = vimmy_getremotephonenum_getphoenum(vimmy_token)
        G_PHONENUM = vimmy_phonenum
        time.sleep(30)
        vimmy_phonetext = vimmy_getremotephonenum_getphoetext(vimmy_token,vimmy_phonenum)
        if(vimmy_phonetext.find("尚未收到") != -1):
            time.sleep(10)
            vimmy_phonetext = vimmy_getremotephonenum_getphoetext(vimmy_token,vimmy_phonenum)
            if(vimmy_phonetext.find("尚未收到") != -1):
                time.sleep(10)
                vimmy_phonetext = vimmy_getremotephonenum_getphoetext(vimmy_token,vimmy_phonenum)

        print('VIMIY自动化脚本：短信原文是：\n')
        print(vimmy_phonetext)
        print('VIMIY自动化脚本：最终的验证码是：\n')
        tmp_handle_str = (vimmy_phonetext[13:])
        ret = re.search("[0-9]{6}",tmp_handle_str)
        tmp_final = ret.group()
        print(tmp_final)
        G_PHONETEXT = tmp_final
    else:
        print('登录短信平台失败\n')


print('VIMIY自动化脚本：登录短信平台，获取手机号\n')
vimmy_token = vimmy_getremotephonenum_login()
#vimmy_token = 'b3c63bc0d43342d9a3321275310b4564'
if(vimmy_token.find("null") == -1):
    vimmy_getremotephonenum_getmoney(vimmy_token)
    vimmy_phonenum = vimmy_getremotephonenum_getphoenum(vimmy_token)
    G_PHONENUM = vimmy_phonenum
    time.sleep(30)
print('VIMIY自动化脚本：打开小红书\n')
adb_click(916,1090)
time.sleep(10)
print('VIMIY自动化脚本：打开手机登录页面\n')
adb_click(487,1664)
time.sleep(5)
print('VIMIY自动化脚本：清空手机号码\n')
adb_click(876,630)
time.sleep(5)
print('VIMIY自动化脚本：输入手机号码\n')
adb_inputtext(G_PHONENUM)
time.sleep(5)

# vimmy_getbaiduimgtext()
# b3c63bc0d43342d9a3321275310b4564