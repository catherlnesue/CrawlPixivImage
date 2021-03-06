# Theme
**Python爬取P站图片**

# CrawlPixivImage
### 程序的一些特点：
* 支持图片下载进度条显示
* 异步加载页面的图片下载
* 支持多进程/线程下载图片

# Disclaimer（免责声明）
> **&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 该程序仅用于个人学习、研究或欣赏。经由该程序下载Pixiv图片的版权归原作者所有。使用该程序的朋友请尊重Pixiv作品原作者，不要将作品用于商业或其他非法用途，所产生的任何结果皆不代表本人立场，本人不对其真实合法性以及版权负责，亦不承担任何法律责任。**

# Program function
* &nbsp;&nbsp;&nbsp;&nbsp; 我将CrawlerPixivImg封装了起来，提供了获取小/中/大图片的链接和下载接口，但需要注意的是只能通过小图片的链接来获取其他尺寸大小的图片接口当通过编写主函数程序来连入接口时，就需要初始化CrawlerPixivImg类，类的初始化的原型是：`__init__(self, url, params, headers)`初始化后就可以 通过类变量访问类中的三个方法`GetSmallImgUrl(self)`、`GetMediumImgUrl(self, urlList)`、`GetLargestImgUrl(self,urlList)`来获得图片的 链接，最后再调用类中的方法`DownloadProcess(self, url, IMGLibrary = {})`进行下载。  
* &nbsp;&nbsp;&nbsp;&nbsp; 多进程部分我并没进行封装，需要自己根据需求编写程序。

# Example
[example.py](https://github.com/darkchii/CrawlPixivImage/blob/master/CrawlPixivImage/example.py)

# How to used
1. Tools: Python version = 3.6.x
2. `git clone https://github.com/darkchii/CrawlPixivImage`
3. Type the command line on the console:
```
cd CrawlPixivImage
python example.py
```

# Run result
![screenshot.png](CrawlPixivImage/Pixiv_Img/screenshot.png)

# About Program
+ &nbsp;&nbsp;&nbsp;&nbsp;写这个程序前花了一个星期补充了一些基础知识，因而参考了不少的资料，实际上我正式学习Python才半个月，所以程序尚且还有很多的不足之处，还希望大家理解与指点!我会通过之后的学习而不断的改进该程序以使其更完美。
> 程序至少需要了解一点`http协议`、`http动词`、`浏览器渲染过程`、`多进程/多线程`、`同步/异步加载`、`python - requesets package`。

# Finally
***Reference material:***
```
1. http://docs.python-requests.org/zh_CN/latest/user/quickstart.html
2. https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001431927781401bb47ccf187b24c3b955157bb12c5882d000
3. https://www.168seo.cn/python/24286.html
```
