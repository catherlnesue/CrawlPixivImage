# crawlpixiv.py
 **该文件中增加了多进程模块，使得程序的使用变得更简易。**
    
  可使用如下方式进行调用：
    [example2.py](example.py)
    ~~~ python
    
    from CPIS.crawlpixiv import CrawlerPixivImg,CrawlProcess
    
    def main():
      user_agent = 'Mozilla/5.0(Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
      img_library = {}
      CrawlProcess(user_agent=user_agent,img_library=img_library).run()

    if __name__ == '__main__':
      start = time.time()
      main()
      end = time.time()
      print('下载用时：{} min'.format((end - start)/60))
    ~~~
