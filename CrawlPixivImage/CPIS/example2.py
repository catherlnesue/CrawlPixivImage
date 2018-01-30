from CPIS.crawlpixiv import CrawlProcess
import time

def main():
    user_agent = 'Mozilla/5.0(Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    img_library = {}
    
    CrawlProcess(user_agent=user_agent,img_library=img_library).run()

if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print('下载用时：{} min'.format((end - start)/60))
