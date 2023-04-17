# pixiv一键下载 ⟵(๑¯◡¯๑)

p站爬虫，以画师pid为参数，一次性下载所有作品(默认为**原图**)  

(部分 **少儿不宜** 图片需要登录(cookie)才能下载)

**#23.4 更新:改用异步重写了一遍,用法不变**

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

**尽量不要一次性下载太多，可能会被封IP**

加了随机useragent，不知道有没有用( ╹▽╹ )...  

杂项
--
如果想要下载其它大小的话，可以把第60行  

`url_lst=[x['urls']['original'] for x in raw_data['body']]`  

里的 **original** 改为其它格式，详情请参考下面这张图:  

![QQ图片20220819000559](https://user-images.githubusercontent.com/57820488/185442305-2259ba81-40ee-43df-8e95-3b2b7d19a4fe.png)  

〜(꒪꒳꒪)〜
