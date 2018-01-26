import time
import base64
import rsa
import binascii
import re
import random
import requests
try:
    from PIL import Image
except:
    pass
try:
    from urllib.parse import quote_plus
except:
    from urllib import quote_plus

# 构造 Request headers
agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0'
headers = {
    'User-Agent': agent
}

session = requests.session()

# 访问 初始页面带上 cookie
index_url = "http://weibo.com/login.php"
try:
    session.get(index_url, headers=headers, timeout=2)
except:
    session.get(index_url, headers=headers)
try:
    input = raw_input
except:
    pass


def get_su(username):
    """
    对 email 地址和手机号码 先 javascript 中 encodeURIComponent
    对应 Python 3 中的是 urllib.parse.quote_plus
    然后在 base64 加密后decode
    """
    username_quote = quote_plus(username)
    username_base64 = base64.b64encode(username_quote.encode("utf-8"))
    return username_base64.decode("utf-8")


# 预登陆获得 servertime, nonce, pubkey, rsakv
def get_server_data(su):
    pre_url = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su="
    pre_url = pre_url + su + "&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)&_="
    pre_url = pre_url + str(int(time.time() * 1000))
    pre_data_res = session.get(pre_url, headers=headers)

    sever_data = eval(pre_data_res.content.decode("utf-8").replace("sinaSSOController.preloginCallBack", ''))

    return sever_data


# print(sever_data)


def get_password(password, servertime, nonce, pubkey):
    rsaPublickey = int(pubkey, 16)
    key = rsa.PublicKey(rsaPublickey, 65537)  # 创建公钥
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)  # 拼接明文js加密文件中得到
    message = message.encode("utf-8")
    passwd = rsa.encrypt(message, key)  # 加密
    passwd = binascii.b2a_hex(passwd)  # 将加密信息转换为16进制。
    return passwd


def get_cha(pcid):
    cha_url = "http://login.sina.com.cn/cgi/pin.php?r="
    cha_url = cha_url + str(int(random.random() * 100000000)) + "&s=0&p="
    cha_url = cha_url + pcid
    cha_page = session.get(cha_url, headers=headers)
    with open("cha.jpg", 'wb') as f:
        f.write(cha_page.content)
        f.close()
    try:
        im = Image.open("cha.jpg")
        im.show()
        im.close()
    except:
        print(u"请到当前目录下，找到验证码后输入")


def login(username, password):
    # su 是加密后的用户名
    su = get_su(username)
    sever_data = get_server_data(su)
    servertime = sever_data["servertime"]
    nonce = sever_data['nonce']
    rsakv = sever_data["rsakv"]
    pubkey = sever_data["pubkey"]
    showpin = sever_data["showpin"]
    password_secret = get_password(password, servertime, nonce, pubkey)

    postdata = {
        'entry': 'weibo',
        'gateway': '1',
        'from': '',
        'savestate': '7',
        'useticket': '1',
        'pagerefer': "http://login.sina.com.cn/sso/logout.php?entry=miniblog&r=http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl",
        'vsnf': '1',
        'su': su,
        'service': 'miniblog',
        'servertime': servertime,
        'nonce': nonce,
        'pwencode': 'rsa2',
        'rsakv': rsakv,
        'sp': password_secret,
        'sr': '1366*768',
        'encoding': 'UTF-8',
        'prelt': '115',
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
        'returntype': 'META'
        }
    login_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
    if showpin == 0:
        login_page = session.post(login_url, data=postdata, headers=headers)
    else:
        pcid = sever_data["pcid"]
        get_cha(pcid)
        postdata['door'] = input(u"请输入验证码")
        login_page = session.post(login_url, data=postdata, headers=headers)
    login_loop = (login_page.content.decode("GBK"))
    # print(login_loop)
    pa = r'location\.replace\([\'"](.*?)[\'"]\)'
    loop_url = re.findall(pa, login_loop)[0]
    # print(loop_url)
    # 此出还可以加上一个是否登录成功的判断，下次改进的时候写上
    login_index = session.get(loop_url, headers=headers)
    uuid = login_index.text
    uuid_pa = r'"uniqueid":"(.*?)"'
    uuid_res = re.findall(uuid_pa, uuid, re.S)[0]
    web_weibo_url = "http://weibo.com/%s/profile?topnav=1&wvr=6&is_all=1" % uuid_res
    weibo_page = session.get(web_weibo_url, headers=headers)
    weibo_pa = r'<title>(.*?)</title>'
    # print(weibo_page.content.decode("utf-8"))
    userID = re.findall(weibo_pa, weibo_page.content.decode("utf-8", 'ignore'), re.S)[0]
    print(u"欢迎你 %s, 你在正在使用 xchaoinfo 写的模拟登录微博" % userID)


from urllib import request, error, parse
import os
from datetime import datetime, timedelta

class CollectData():

    def __init__(self, keyword, startTime, endTime, saveDir, interval = '5', baseUrl = "http://s.weibo.com/weibo/"):
        self.baseUrl = baseUrl;
        self.setKeyword(keyword);
        self.setTimeStamp(startTime, endTime);
        self.setSaveDir(saveDir);
        self.setInterval(interval);

    def setKeyword(self, keyword):
        self.keyword = keyword
        # print ('encode twice: ', self.getKeyword())

    def setTimeStamp(self, startTime, endTime):
        self.startTime = startTime
        self.endTime = endTime

    def setSaveDir(self, saveDir):
        self.saveDir = saveDir
        if not os.path.exists(saveDir):
            os.mkdir(self.saveDir)

    def setInterval(self, interval):
        self.interval = int(interval)

    def getKeyword(self):
        once = parse.urlencode({'kw': self.keyword})[3:]
        return parse.urlencode({'kw': once})[3:]

    def getUrl(self):
        return self.baseUrl+self.getKeyword()+'&typeall=1&suball=1&timescope=custom:'+self.startTime+':'+self.endTime+"&page="

    def downloadData(self, url):
        hasMorePage = True
        pageNum = 1
        while hasMorePage and pageNum < 51:
            time.sleep(self.interval)
            # print ('----------------------------------page ' + str(pageNum) + ' ----------------------------------\n')
            pageUrl = url + str(pageNum)
            pageData = ''
            try:
                # print ('pageUrl: ' + pageUrl)
                pageHTML = session.get(pageUrl)
                # print ('type of pagehtml:', type(pageHTML))
                pageData = pageHTML.text
                # print ('type of pagedata:', type(pageData))
                if pageData.find('noresult_tit') != -1:
                    # print("This page has no result")
                    hasMorePage = False
                    print('Totally have', str(pageNum-1), 'pages')
                    print('Success:', str(len(os.listdir(self.saveDir))),'\tFail:', str(pageNum-1-len(os.listdir(self.saveDir))))
                    break
                lines = pageData.splitlines()
                for line in lines:
                    if line.startswith('<script>STK && STK.pageletM && STK.pageletM.view({"pid":"pl_weibo_direct"'):
                        # print ("Successfully get query result")
                        n = line.find('html":"')
                        if n > 0:
                            try:
                                outData = line[n + 7 : -12]
                                fout = open(self.saveDir + os.sep + str(pageNum) + '.txt', 'w')
                                fout.write('------------------------------result------------------------------\n')
                                fout.write(outData)
                                # print ("Write data successfully")
                                fout.close()
                            except UnicodeEncodeError as e:
                                # print ('UnicodeError happens:', e)
                                continue
            except:
                pass
            pageNum += 1

def main():
    username = input(u'用户名：')
    password = input(u'密码：')
    login(username, password)
    while True:

        keyword = input('Enter the keyword(type \'quit\' to exit ):')
        if keyword == 'quit':
            sys.exit()
        startTime = input('Enter the start time(Format:YYYY-mm-dd-HH):')
        endTime = input('Enter the end time(Format:YYYY-mm-dd-HH):')
        savedir = input('Enter the save directory(Like ./data):')
        interval = input('Enter the time interval( >30 and deafult:50):')
        startTime_stamp = startTime
        endTime_stamp = startTime

        # example:
        # keyword = '江哥案'
        # startTime = '2017-11-10-00'
        # endTime = '2017-12-31-00'
        # interval = 5

        # 设定时间间隔为1天搜索
        while True:
            endTime_stamp = (datetime.strptime(endTime_stamp,'%Y-%m-%d-%H') + timedelta(days = 1)).strftime('%Y-%m-%d-%H')
            if endTime_stamp > endTime:
                break
            savedir = './data/'+startTime_stamp+'_'+endTime_stamp
            instance = CollectData(keyword, startTime_stamp, endTime_stamp, savedir, interval)

            while True:
                print ('-'*5, instance.startTime, 'to', instance.endTime, '-'*5)
                url = instance.getUrl()
                print ('Start downloading data', '.'*6)
                start_download_time = datetime.now()
                instance.downloadData(url)
                end_download_time = datetime.now()
                print ('Time cost:', end_download_time-start_download_time)
                break
            startTime_stamp = (datetime.strptime(startTime_stamp,'%Y-%m-%d-%H') + timedelta(days = 1)).strftime('%Y-%m-%d-%H')
            time.sleep(20)
        break

if __name__ == '__main__':
    main()