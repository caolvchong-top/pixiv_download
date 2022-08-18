import requests
from fake_useragent import UserAgent
import re
from multiprocessing import Pool
import json
import os

class Artist_download():
    def __init__(self,pid:str,cookie:str=None,proxies:str=None):
        self.ua=UserAgent()
        self.pid=pid
        self.artist_url='https://www.pixiv.net/ajax/user/'+self.pid+'/profile/all?lang=zh'
        self.headers={}     #考虑到可能要传进来cookie，所以下面改用copy调用
        self.proxies=proxies
        if cookie:
            self.headers['cookie']=cookie

        artwork_id_lst=self.get_all_id()

        if not os.path.exists(str(self.pid)):
            os.makedirs(str(self.pid))

        pool=Pool()     #开个进程池
        for i in artwork_id_lst:
            pool.apply_async(get_all,args=(i,self.headers,self.pid,self.proxies,))
        pool.close()
        pool.join()

    def get_all_id(self):
        _headers=self.headers.copy()
        _headers['user-agent']=self.ua.random
        _headers['referer']='https://www.pixiv.net/users/'+self.pid
        keep=True
        while keep:
            try:
                response=requests.get(self.artist_url,headers=_headers,proxies=self.proxies).text
                keep=False
            except Exception as e:
                pass
        raw_data=json.loads(response)
        if raw_data['body']['illusts']:
            illusts_lst=list(raw_data['body']['illusts'].keys())
        else:
            illusts_lst=[]
        if raw_data['body']['manga']:
            manga_lst=list(raw_data['body']['manga'].keys())
        else:
            manga_lst=[]
        id_lst=illusts_lst+manga_lst      #该作者所有的插画+漫画id
        
        return id_lst

## 突然发现Pool没法执行实例方法，只能把这部分拆出来了

def get_all(artwork_id:str,headers,pid,proxies):       #传入单个作品id，获取真实url，启动下载
    _ua=UserAgent()
    _headers=headers.copy()
    _headers['user-agent']=_ua.random
    _headers['referer']='https://www.pixiv.net/artworks/'+artwork_id
    true_url_lst=get_artwork_url(artwork_id,_headers,proxies)
    filename_re='img/(\d*)/(\d*)/(\d*)/\d+/\d+/\d+/(.*)'       #用来生成文件名
    for url in true_url_lst:        #开始下载
        file_name='_'.join(re.findall(filename_re,url)[0])
        file_path=pid+'/'+file_name
        keep=True
        while keep:
            try:
                response=requests.get(url,headers=_headers,proxies=proxies).content
                keep=False
            except Exception as e:
                pass
        with open(file_path,'wb') as f:
            f.write(response)
            f.close()
        print('%s===>下载完成'%file_name)       ##如果不需要输出信息可以把这行删掉##

def get_artwork_url(artwork_id,headers,proxies):       #获取单个作品的链接(主要是为了找出分p的地址)
    _url='https://www.pixiv.net/ajax/illust/'+artwork_id+'/pages?lang=zh'

    keep=True
    while keep:
        try:
            response=requests.get(_url,headers=headers,proxies=proxies).text
            keep=False
        except Exception as e:
            pass
    raw_data=json.loads(response)
    url_lst=[x['urls']['original'] for x in raw_data['body']]
    return url_lst
    

#Test
if __name__=='__main__':
    #multiprocessing.freeze_support()       #用pyinstaller打包的时候带上这一行
    pid=input('请输入作者pid：')
    #pid='7238253'
    login=input('\n是否需要登录(y/n) :')
    if login.lower()=='y':
        cookie=input('\n请把cookie粘贴进来 :')
    else:
        cookie=None
    if_proxy=input('\n是否添加代理[机器能直连pixiv的就不用](y/n) :')
    if if_proxy.lower()=='y':
        msg='''\n1.使用爬虫代理的，请按照requests_proxies格式输入(字典形式)\n
2.本机开了VPN的，请按照{'https':'127.0.0.1:<port>'}格式输入(把<port>换成VPN代理的端口)\n
请输入:'''
        proxies=eval(input(msg))
    else:
        proxies=None

    print('\n如果长时间没看到输出信息，那大概率是出错了，请检查参数输入是否正确...\n')
    a=Artist_download(pid,cookie,proxies)