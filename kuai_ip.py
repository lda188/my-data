def kuaiip():#http://dps.kdlapi.com/api/getdps/?orderid=917060752480178&num=1&pt=1&sep=1
    pool = "http://dps.kdlapi.com/api/getdps/?orderid=917060752480178&num=1&pt=1&sep=1" 
    pool1 = requests.get(url=pool, headers={'User-Agent':UserAgent().random})
    nice_IP = BeautifulSoup(pool1.text,'lxml').p.text
    #pool2 = BeautifulSoup(pool1.text,'lxml')
    #nice_IP = [i.text  for i in pool2.findAll("proxy")] 
    return nice_IP

# ip池初始化
nice_IP = []

# ip池分流 = ip1中转 ；iP2请求
ip1 = nice_IP[6:].copy()

while 5-len(ip1) != 0:
    sat_man_()

 ip2 = ip1[0:4].copy() 

#装入废弃IP
Abandon_ip = []

def Room_page__IP(url1):
    global ip2
    global ip1
    import random
    #连接失败则将该IP踢出队列,继续用后面的ip接入
    count = 0
    while count < 3:
        count +=1 
        try:# 用ip2 队列末位ip 使用
            s = requests.session()
            s.keep_alive = False
            response = s.get(url=url1, headers={'User-Agent':UserAgent().random},proxies = {'https': "https://"+ip2[-1]},timeout=3)
            soup1 = BeautifulSoup(response.text,'lxml')
            bs64Str = re.findall("charset=utf-8;base64,(.*?)'\)", response.text)[0] 
            response.close()
            del(response)
            
            break
        except:
            print("动态IP,最多替换3词，第%d次 ... ..."%count)
            global Abandon_ip 
            Abandon_ip.append(ip2[-1])
            
            if len(ip1)<6:
                sat_man_()#补充代理IP再继续爬取
            del ip2[-1] # ip失效 剔除
            if len(ip2)<4:# 保证ip2 队列有至少有 4个ip
                ip2.insert(0,ip1[0])#<10个将待定ip1队列  加入iP2 使用
                del ip1[0]#剔除ip1 中的投入使用的iP  
                if len(ip1)<4:
                    sat_man_()#补充代理IP再继续爬取
                else:
                    pass
            else:
                pass
        finally:
            pass
        
        try:
            return bs64Str,soup1
        except:
            print("请求失败。。。。")
        finally:
            pass