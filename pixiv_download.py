import os
import asyncio
import json
import httpx
import aiofiles
import re
from fake_useragent import UserAgent
import time

class Artist_download():
    def __init__(self,pid: str,cookie: str):
        self.pid=pid
        self.ua=UserAgent()
        self.headers={}
        self.artist_url='https://www.pixiv.net/ajax/user/'+pid+'/profile/all?lang=zh'   #获取该作者作品id列表
        if cookie:
            self.headers['cookie']=cookie
        print('开始提取链接...')
        artwork_id_lst=self.get_all_id()
        if not os.path.exists(str(self.pid)):
            os.makedirs(str(self.pid))
        print('准备下载...')
        self.down_save(artwork_id_lst)  #下载&保存
        print('\n全部完成...')
        
        
    def get_all_id(self):
        _headers=self.headers.copy()
        _headers['user-agent']=self.ua.random
        _headers['referer']='https://www.pixiv.net/users/'+self.pid
        raw_data=httpx.get(self.artist_url,headers=_headers)
        raw_data=raw_data.json()
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

    def down_save(self,id_lst :list):
        #moudle 1,2,3 : 获取链接,下载,保存 --链式
        #----------------------------------------#
        async def moudle_1(id):
            #1.请求、获取下载链接(包括分P链接),链接传给moudle2
            _url='https://www.pixiv.net/ajax/illust/'+id+'/pages?lang=zh'
            _headers=self.headers.copy()
            _headers['user-agent']=self.ua.random
            _headers['referer']='https://www.pixiv.net/artworks/'+id
            url_lst=[]

            async with httpx.AsyncClient() as client:
                try:
                    raw_data=await client.get(_url,headers=_headers)
                    raw_data=raw_data.json()
                    url_lst=[x['urls']['original'] for x in raw_data['body']]       #默认下载original,可选大小:["thumb_mini","small","regular"]
                except Exception:
                    pass
            if url_lst:
                _tasks=[asyncio.create_task(moudle_2(url,_headers)) for url in url_lst]
                await asyncio.gather(*_tasks)

        async def moudle_2(url,headers):
            #2.启动下载，数据传给moudle3
            filename_re='img..(\d*)..(\d*)..(\d*)..\d+..\d+..\d+..(.*)'
            file_name='_'.join(re.findall(filename_re,url)[0])
            async with httpx.AsyncClient() as client:
                try:
                    _data=await client.get(url,headers=headers)
                    await asyncio.gather(moudle_3(_data,file_name))
                except Exception:
                    pass

        async def moudle_3(data,file_name):
            #3.保存图片
            file_path=self.pid+'/'+file_name
            async with aiofiles.open(file_path,'wb') as f:
                await f.write(data.content)
                f.close()
            print(file_path,'===>下载完成')     ##如果不需要输出信息可以把这行删掉##

        #----------------------------------------#

        async def main():
            tasks=[asyncio.create_task(moudle_1(id)) for id in id_lst]
            await asyncio.gather(*tasks)

        asyncio.run(main())

if __name__=='__main__':
    pid=input('输入画师pid:')
    cookie=None
    if input('是否登录[cookie形式](y/n):').lower()=='y':
        cookie=input('cookie:')
    start=time.time()
    a=Artist_download(pid,cookie)
    end=time.time()
    print('耗时:',end-start,'S')
    input('任意键退出...')

