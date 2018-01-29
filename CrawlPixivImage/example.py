'''
@Author        : darkchii
@Create date   : 2018-01-21
@Theme         : WebCrawler - CrawlPixivImage
'''

from multiprocessing import Pool,cpu_count
import time
from CPIS.crawlimage import CrawlerPixivImg
import os


def example():
    if not os.path.exists('Pixiv_Img'):
        print('请在该程序目录下创建一个\'Pixiv_Img\'文件夹后再运行该程序!')
        os._exit(1)

    try:
        with open('Pixiv_Img/url.txt', 'a'):
            pass
    except FileNotFoundError:
        with open('Pixiv_Img/url.txt', 'w'):
            pass

    img_library = {}
    init_url = 'https://www.pixiv.net/ranking.php?mode=daily'
    for date in range(20180128,20180130):   # 排行榜日期
        # bug update:如果日期为当天排行榜 则 url 格式为 https://www.pixiv.net/ranking.php?mode=daily&p=页码&format=json&tt=6a124b46e04507dcee2efed9bac25cf5
        for p in range(1,4):   # 异步加载的页面大概有几十页 每一页共50个小图片链接 这里随意测试 而且排行榜中会有前几天甚至前几百天的图片 所以会有许多重复的图片 因此实际上没必要把一张排行榜的全部爬完
            # url格式：https://www.pixiv.net/ranking.php?mode=daily&date=日期&p=页码&format=json&tt=6a124b46e04507dcee2efed9bac25cf5
            params = {
                'date':str(date),
                'p':str(p),
                'format':'json',
                'tt':'6a124b46e04507dcee2efed9bac25cf5'
            }
            
            if str(date) == time.strftime('%Y%m%d', time.localtime()):
                params.pop('date')

            headers = {
                'Referer': 'https://www.pixiv.net/ranking.php?mode=daily&date={}'.format(str(date)),
                'User-Agent': 'Mozilla/5.0(Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
            }

            page = CrawlerPixivImg(init_url, params=params, headers=headers)    # 初始化
            small_img_url_list = page.get_small_img_url()
            pixiv_img_url_list = page.get_largest_img_url(small_img_url_list)

            Process = Pool(cpu_count())   #  一般默开启电脑CPU核心个数 这里用多进程下载比多线程快很多
            for url in pixiv_img_url_list:
                Process.apply_async(page.download_pixiv_img, args=(url, img_library))
            Process.close()
            Process.join()


if __name__ == '__main__':
    print(__doc__)
    start = time.time()
    example()
    end = time.time()
    print('此次下载用时:{} min'.format(float(end - start)/60))
