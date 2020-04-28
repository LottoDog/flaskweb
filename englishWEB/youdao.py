# coding=utf-8 
import time
import random
import requests
# hashlib有很多种加密方法
from hashlib import md5


def get_ts_bv_salt_sign(word):
    # e为翻译的字符串
    e = word
    # ts13为时间戳
    ts = r = str(int(time.time()) * 1000)
    print("ts = r = ", str(int(time.time()) * 1000))

    # bv=t-->为User-agent 字符串Mozilla/后进行md5加密
    string = '5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
    # 创建加密对象
    s = md5()
    # 参数要bytes
    s.update(string.encode())
    # 获取十六进制加密结果
    bv = t = s.hexdigest()
    print("bv= t = ", t)

    # 产生i
    salt = i = r + str(random.randint(0, 9))
    print("salt= i=", salt)

    # sign: n.md5("fanyideskweb" + e + i + "@6f#X3=cCuncYssPsuRUE")
    ssign = md5()
    #   n%A-rKaT5fb[Gy?;N5@Tj
    sstring = "fanyideskweb" + e + i + "n%A-rKaT5fb[Gy?;N5@Tj"
    ssign.update(sstring.encode())
    sign = ssign.hexdigest()
    print("sign = ", sign)
    return salt, sign, ts, bv


def attack_YD(word):
    salt, sign, ts, bv = get_ts_bv_salt_sign(word)
    url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    # 定义headers:
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Length": "251",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": '''_ntes_nnid=16740018c235ab7bd6e72431317b9f7e,1557720834906; OUTFOX_SEARCH_USER_ID_NCOO=1680126164.859171; OUTFOX_SEARCH_USER_ID="867705397@10.168.11.15"; JSESSIONID=aaaFbFsrRaUsKgcJXRgSw; ___rl__test__cookies=1559199247140''',
        "Host": "fanyi.youdao.com",
        "Origin": "http://fanyi.youdao.com",
        "Referer": "http://fanyi.youdao.com/",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    # Form表单数据
    data = {
        "i": word,
        "from": "AUTO",
        "to": "AUTO",
        "smartresult": "dict",
        "client": "fanyideskweb",
        "salt": salt,
        "sign": sign,
        "ts": ts,
        "bv": bv,
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "action": "FY_BY_REALTlME",
    }
    # 注意要用post请求
    res = requests.post(
        url=url,
        headers=headers,
        data=data,
    )
    res.encoding = 'utf-8'
    

    #检查
    print(type(res.json()))
    if res.json() == {'errorCode': 40}:
        print('!!!!!!!!!!!!!!!')
        return '您输入的翻译内容不合法，请重新尝试'
    else:
        try:
            print('\n', word, ':', res.json()['translateResult'][0][0]['tgt'])
        except Exception:
            return '您输入的翻译内容不合法，请重新尝试'

        try:
            
            sw = []
            for i in res.json()['smartResult']['entries']:
                #排空
                if i and i != '  \r\n':
                    i.replace('\n', '').replace('\r', '')
                    


                    sw.append(i)
            
        except Exception:
            pass
        return res.json()['translateResult'][0][0]['tgt'], sw

## 独立模式解除下方
# # 反爬检查最多的就是：User-agent;Cookie;Referer;
# if __name__ == "__main__":
#     word = input("请输入翻译的字符：")
#     attack_YD(word)
