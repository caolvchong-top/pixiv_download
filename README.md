# pixiv一键下载 ⟵(๑¯◡¯๑)

p站爬虫，以画师pid为参数，一次性下载所有作品(默认为**原图**)  

(部分 **少儿不宜** 图片需要登录(cookie)才能下载)

部署
--

**linux** 要先装一下依赖:

`cd pixiv_download`

`pip3 install -r requirements.txt`

运行:

`python3 pixiv_download.py`  

**windows** 可以去release里用打包好的版本

注意事项
--

![QQ图片20220818234105](https://user-images.githubusercontent.com/57820488/185437033-b494a4a7-3f82-4941-a213-419a0ded2b85.png)

**代理格式**  
1.  
`{'https':'代理地址'}`

2.本机开了VPN的请按下面这个格式填  
`{'https':'127.0.0.1:<port>'}`  

例：  
`{'https':'127.0.0.1:8888'}`  


**尽量不要一次性下载太多，可能会被封IP**

加了随机useragent，不知道有没有用( ╹▽╹ )...  

杂项
--
如果想要下载其它大小的话，可以把第88行  

`url_lst=[x['urls']['original'] for x in raw_data['body']]`  

里的 **original** 改为其它格式，详情请参考下面这张图:  

![QQ图片20220819000559](https://user-images.githubusercontent.com/57820488/185442305-2259ba81-40ee-43df-8e95-3b2b7d19a4fe.png)  

〜(꒪꒳꒪)〜
