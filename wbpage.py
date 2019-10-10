import  pymysql
import pandas as pd 
from sqlalchemy import create_engine
from fake_useragent import UserAgent 
import base64
from bs4 import BeautifulSoup
from io import BytesIO
from fontTools.ttLib import TTFont
import requests
import re 
import time 




# 当前网页信息
def Room_page_():
    a = Room_cell_(1)[6] 
    pages = []
    for i in range(a-1):
        pages.append(Room_cell_(i))
    pages = pd.DataFrame(pages,columns=["title","space","place","source","pul_time","price","pages_number_type"])
    return pages 



#发出请求获得 bs64Str,soup1
def Room_page__(url):
    requests.adapters.DEFAULT_RETRIES = 5 # 增加重连次数
    s = requests.session()
    s.keep_alive = False
    
    response = s.get(url=url, headers={'User-Agent':UserAgent().random}) 
    bs64Str = re.findall("charset=utf-8;base64,(.*?)'\)", response.text)[0] 
    soup1 = BeautifulSoup(response.text,'lxml')
   
    response.close()
    del(response)
    
    return bs64Str,soup1

# 数据列表
def data_cell(soup1):
    des_ = soup1.find_all(attrs={'class': 'des'})
    price_time = soup1.find_all(attrs={'class': 'list-li-right'})
    return des_,price_time



# 单个房间信息
def room_cell(i,soup1):
    des_,price_time= data_cell(soup1)
    lebgth = len(des_)
    re_ =re.compile(r'\n (.*?) \n') 
    title = re_.findall(des_[i].h2.text)[0].replace(" ","")
    
    space = des_[i].p.text.replace(" ","")
    
    p1 = des_[i].find_all("a")[1].text 
    p2 = des_[i].find_all("a")[2].text 
    place = p1 + "-" + p2
    
    try:
        source1 = des_[i].find_all(attrs={'class': 'jjr'})[0]
        re1_ =re.compile(r'[\u4e00-\u9fa5]+')
        source = re1_.findall(str(source1).replace(" ",""))
    except:
        source = 'None'
    finally:
        pass
    try:
        T = price_time[i].find_all(attrs={'class': 'send-time'})[0].text
        if T == "\n":
            T = "None"
        else:
            T = T.replace("\n","").replace(" ","")   
    except:
        T = "None"
    finally:
        pass
        
    price =price_time[i].find_all(attrs={'class': 'strongbox'})[0].text
    
    return [title,space,place,source,T,price,lebgth] 

# 来源
def source_(source):
    source_ = ""
    for i in source:
       source_ += i+"—"
    return source_



# 字体加密解密问题处理
def Font_decode(getText):
    #获取加密字体文件
    #bs64Str = re.findall("charset=utf-8;base64,(.*?)'\)", response.text)[0]
    #解码字体文件
    binData = base64.decodebytes(bs64Str.encode())
    #设置中转路径
    filePath01 = r'C:\Users\ZGL\Desktop\jiemi_20190402_03.otf'
    #中转路径 写入otf字体文件
    with open(filePath01, 'wb') as f:
            f.write(binData)
            f.close()
    # 解析字体库
    font01 = TTFont(filePath01)
    # 解密还原真实字符
    uniList = font01['cmap'].tables[0].ttFont.getGlyphOrder()
    utfList = font01['cmap'].tables[0].ttFont.tables['cmap'].tables[0].cmap

    retList = []
    for i in getText:
        if ord(i) in utfList:
            text = int(utfList[ord(i)][-2:]) - 1
        else:
            text = i
        retList.append(text)
    crackText = ''.join([str(i) for i in retList])
    return  crackText 



#单个房间数据解密
def Room_cell_(i):
    cell = room_cell(i,soup1)
    cell[3] = source_(cell[3])
    cell[0] = Font_decode(cell[0])
    cell[1] = Font_decode(cell[1])
    cell[5] = Font_decode(cell[5])
    return cell











