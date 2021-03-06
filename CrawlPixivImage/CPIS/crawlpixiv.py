from multiprocessing import Pool
from tqdm import tqdm
import re,os,time
import requests

class CrawlerPixivImg(object):
    __chunk_size = 1024

    def __init__(self, url, params, headers):
        object.__init__(self)
        self.url = url
        self.params = params
        self.headers = headers

    def get_small_img_url(self):
        r = requests.get(self.url, params=self.params, headers=self.headers, timeout=1)
        # print(r.url)
        json_file = r.json()['contents']    # 处理json文件
        cut_url = re.compile(r'\'url\': \'(.+?.jpg)\'')
        small_img_url_list = cut_url.findall(str(json_file))
        return small_img_url_list

    def get_medium_img_url(self, urlList):# https://i.pximg.net/c/600x600/img-master/img/2018/01/17/13/33/41/66832795_p0_master1200.jpg
        medium_img_url_list = []
        for url in urlList:
            medium_img_url_list.append(url.replace('240x480', '600x600'))
        return medium_img_url_list

    def get_largest_img_url(self, urlList):# https://i.pximg.net/img-original/img/2018/01/17/13/33/41/66832795_p0.jpg
        largest_img_url_list = []
        for url in urlList:
            largest_img_url = url.replace('c/240x480/img-master','img-original')
            largest_img_url_list.append(largest_img_url.replace('_master1200',''))
        return largest_img_url_list

    def __show_progress_bar(self,url,headers,img_name):
        img_size = requests.get(url, headers=headers, timeout=1).headers['content-length']

        progress_bar = tqdm(
            total=int(img_size),
            initial=0,
            unit='B',
            unit_scale=True,
            desc=img_name
        )

        with requests.get(url, headers=headers, stream=True) as img:
            with open('Pixiv_Img/{}'.format(img_name), 'wb') as fp:
                for chunk in img.iter_content(chunk_size=self.__chunk_size):
                    if chunk:
                        fp.write(chunk)
                        progress_bar.update(self.__chunk_size)
                progress_bar.close()

    def download_pixiv_img(self, url, img_name_library = {}):
        img_name = url.split('/')[-1]
        img_id = img_name[:8]

        headers = {
            'Referer': 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id=' + img_id,
            'User-Agent': 'Mozilla/5.0(Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }

        response_status = requests.get(url, headers=headers, timeout=1).status_code

        if response_status != (404 or 403):

            if img_name in img_name_library:   # 如果已经下载图片 则退出函数
                print('The same picture exists!')
                return

            with open('Pixiv_Img/url.txt', 'a') as fp:
                fp.write(img_name + ':')

            with open('Pixiv_Img/url.txt', 'a') as fp:
                fp.write(str(url) + '\r\n')

            self.__show_progress_bar(url,headers,img_name)

            dict = {img_name: img_id}
            img_name_library.update(dict)

        if response_status == (404 or 403):  # 如果jpg格式图片错误 则用png格式保存
            url = url.replace('jpg','png')

            response_status = requests.get(url, headers=headers, timeout=1).status_code
            if response_status == (404 or 403):  # 如果图片格式不是jpg 或 png 则退出
                print('图片格式不支持下载或者链接被禁止访问!')
                return

            img_name = url.split('/')[-1]
            img_id = img_name[:8]
            headers = {
                'Referer': 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id=' + img_id,
                'User-Agent': 'Mozilla/5.0(Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
            }

            if img_name in img_name_library:
                print('The same picture exists!')
                return

            with open('Pixiv_Img/url.txt', 'a') as fp:
                fp.write(img_name + ':')

            with open('Pixiv_Img/url.txt','a') as fp:
                fp.write(str(url) + '\r\n')

            self.__show_progress_bar(url,headers,img_name)

            dict = {img_name:img_id}
            img_name_library.update(dict)
            

class CrawlProcess(object):
    __init_url = 'https://www.pixiv.net/ranking.php?mode=daily'

    def __init__(self,start_date=None,end_date=None,end_page=None,user_agent='',img_library = {}):
        object.__init__(self)
        if not os.path.exists('Pixiv_Img'):
            print('请在该程序目录下创建一个\'Pixiv_Img\'文件夹后再运行该程序!')
            os._exit(1)

        try:
            with open('Pixiv_Img/url.txt', 'a'):
                pass
        except FileNotFoundError:
            with open('Pixiv_Img/url.txt', 'w'):
                pass

        self.start_date = start_date
        self.end_date = end_date
        self.end_page = end_page
        self.user_agent = user_agent
        self.img_library = img_library

    def run(self):

        if not(self.start_date and self.end_date):
            self.start_date = self.end_date = int(time.strftime('%Y%m%d', time.localtime()))

        if self.start_date == None and self.end_date != None:
            self.start_date = self.end_date

        if self.end_date == None and self.start_date != None:
            self.end_date = self.start_date

        if self.end_page == None:
            self.end_page = 1

        for date in range(self.start_date, self.end_date + 1):  # 排行榜日期
            for p in range(1,self.end_page + 1):
                # https://www.pixiv.net/ranking.php?mode=daily&date=日期&p=页码&format=json&tt=6a124b46e04507dcee2efed9bac25cf5
                params = {
                    'date': str(date),
                    'p': str(p),
                    'format': 'json',
                    'tt': '6a124b46e04507dcee2efed9bac25cf5'
                }

                if str(date) == time.strftime('%Y%m%d', time.localtime()):
                    params.pop('date')

                headers = {
                    'Referer': 'https://www.pixiv.net/ranking.php?mode=daily&date={}'.format(str(date)),
                    'User-Agent': self.user_agent
                }

                Page = CrawlerPixivImg(self.__init_url, params=params, headers=headers)
                small_img_url_list = Page.get_small_img_url()
                pixiv_img_url_list = Page.get_largest_img_url(small_img_url_list)

                Process = Pool(os.cpu_count())
                for url in pixiv_img_url_list:
                    Process.apply_async(Page.download_pixiv_img, args=(url, self.img_library))
                Process.close()
                Process.join()
