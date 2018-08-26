# weibo_search

## EN

This project uses Weibo's advanced search to implement keyword-based content crawlers.

![alt text](https://cn-albertwu96.github.io/img/process.png "process")

## Crawl Html page

> This part of the code is integrated in downloadData.py

The first part simulates user login, using [fuck-login](https://github.com/xchaoinfo/fuck-login/blob/master/007%20weibo.com/weibo.com.py) provided by xchaoinfo. The way to log in is very simple. The cookie can be saved in a file after a successful login. If you need it later, you can use the requests to read the cookie file to crawl the microblog.

The second part is to use Sina's advanced search function to search for Sina Weibo data of Khan keywords, [code reference](http://blog.csdn.net/heloowird/article/details/38149451), in this piece needs to engage Clear the composition of the address bar url.

## Extract key content in html page

> This part of the code is integrated in extractData.py

The first part uses lxml's etree to implement html parsing and reading storage.

The second part of the unicode_escape transcoding, to ensure that the Chinese display is normal with a text editor.

## How to run

```
$ python downloadData.py
$ ls
data    downloadData.py    extractData.py
$ ls data
2017-11-10-00_1027-11-11-00    ...
$ ls 2017-11-10-00_1027-11-11-00
1.txt    ...
$ python extractData.py
$ ls
data    downloadData.py    extractData.py    final.csv
```

## CN

本项目利用微博的高级搜索实现基于关键词的内容爬虫

![alt text](https://cn-albertwu96.github.io/img/process.png "process")

## html页面抓取

> 此部分代码整合在downloadData.py

第一部分模拟用户登录，使用了xchaoinfo提供的[fuck-login](https://github.com/xchaoinfo/fuck-login/blob/master/007%20weibo.com/weibo.com.py).这种方式的登录十分简便。可以在成功登录之后会将cookie保存在文件中。如果后续需要，可以直接用requests读取cookie文件即可对微博爬虫。

第二部分是利用微博的高级搜索功能搜索汗关键词的新浪微博数据，[代码参考](http://blog.csdn.net/heloowird/article/details/38149451)，在这一块需要搞清楚地址栏url的组成特征即可。

## html页面关键内容提取

> 此部分代码整合在extractData.py

第一部分利用lxml的etree实现html解析读取存储。

第二部分进行unicode_escape转码，确保用文本编辑器打开中文正常显示。

## 运行说明

```
$ python downloadData.py
$ ls
data    downloadData.py    extractData.py
$ ls data
2017-11-10-00_1027-11-11-00    ...
$ ls 2017-11-10-00_1027-11-11-00
1.txt    ...
$ python extractData.py
$ ls
data    downloadData.py    extractData.py    final.csv
```