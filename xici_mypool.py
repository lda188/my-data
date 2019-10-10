import requests 
from bs4 import BeautifulSoup 
import pandas as pd 
import re
import random
import time
import numpy as np
from fake_useragent import UserAgent 
# 获取西刺IP
def xici_ip(strat,end):
    """输入形式参数：从第strat页开始，end页结束:
    eg : http,https = xici_ip(strat,end)"""
    url_1 = 'https://www.xicidaili.com/nn/'
    xc_ip_Pool=pd.DataFrame()
    for j in range(strat-1,end):
        try:
            print("爬取 第%d页  ......"%(j+1)) 
            if j == 0:
                url = url_1
            else:
                url=url_1+str(j)

            #服务器请求设置0
            requests.adapters.DEFAULT_RETRIES = 5 # 增加重连次数
            s = requests.session()
            s.keep_alive = False # 关闭多余连接

            response_ip = s.get(url,headers={'User-Agent':UserAgent().random})
            soup_ip = BeautifulSoup(response_ip.text,'lxml')

            xc_ip_=[]
            for i in range(1,len(soup_ip.select('tr'))): 
                b = soup_ip.select('tr')[i].select('td')[1].text
                c = soup_ip.select('tr')[i].select('td')[2].text
                a = soup_ip.select('tr')[i].select('td')[5].text.lower()           
                xc_ip_.append([a,b,c])
            xc_ip=pd.DataFrame(xc_ip_,columns=["a","b","c"])
            #关闭上一次服务器请求 释放内存
            response_ip.close()
            del(response_ip)
            xc_ip_Pool=pd.concat([xc_ip_Pool,xc_ip],ignore_index=True)
            time.sleep(random.randint(3,5))
        except Exception:
            print('An error or warning occurred:')
        finally:
            time.sleep(random.randint(2,5))
    https = xc_ip_Pool[xc_ip_Pool.a == "https"]
    https.index=range(len(https.a))
    http = xc_ip_Pool[xc_ip_Pool.a == "http"]
    http.index=range(len(http.a))
    print("结束！")
    
    return http,https


# 检测 http 中 IP有效性 #返回数组（索引时间）
def valid_IP(http): 
   # """传入HTTP协议对应的代理IP，以及每个IP的响应时间参数：“T"，由xici_ip(strat,end)获得：
   # eg: valid_ip = valid_IP(https,5)"""
    #print("最多等待%d 分钟！"%int((http.shape[0]*T)/60))
    import pandas as pd
    import telnetlib
    import time
    valid_ip = []
    for i in range(http.shape[0]):
        try:
            start = time.clock()
            telnetlib.Telnet(http.b[i], port=http.c[i], timeout=3)
            IP = http.a[i] + "://" + http.b[i] + ":" + http.c[i]
            elapsed = (time.clock() - start)
            valid_ip.append([IP,elapsed])
        except:
            pass
        finally:
            pass
    valid_ip = pd.DataFrame(valid_ip,columns=["ip","ratio"])
    valid_ip = valid_ip.sort_values(by="ratio")
    valid_ip.index = range(valid_ip.shape[0])
    return valid_ip