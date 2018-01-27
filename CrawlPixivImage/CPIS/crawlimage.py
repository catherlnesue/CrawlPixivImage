import requests
from tqdm import tqdm
import re

class CrawlerPixivImg(object):
    def __init__(self, url, params, headers):
        object.__init__(self)
        self.url = url
        self.params = params
        self.headers = headers

    def GetSmallImgUrl(self):   # 解决异步加载机制
        r = requests.get(self.url, params=self.params, headers=self.headers)
        # print(r.url)
        Elem = str(r.json()['contents'])    # 自动处理json文件
        recmp = re.compile(r'\'url\': \'(.+?.jpg)\'')   # 从json文件中获取所有小图片的url存放到列表中
        SmallImgUrlList = recmp.findall(Elem)
        return SmallImgUrlList

    def GetMediumImgUrl(self, urlList):# https://i.pximg.net/c/600x600/img-master/img/2018/01/17/13/33/41/66832795_p0_master1200.jpg
        MediumImgUrlList = []
        for url in urlList:
            MediumImgUrlList.append(url.replace('240x480', '600x600'))
        return MediumImgUrlList

    def GetLargestImgUrl(self, urlList):# https://i.pximg.net/img-original/img/2018/01/17/13/33/41/66832795_p0.jpg
        LargestImgUrlList = []
        for url in urlList:
            LargestImgUrl = url.replace('c/240x480/img-master','img-original')
            LargestImgUrlList.append(LargestImgUrl.replace('_master1200',''))
        return LargestImgUrlList

    def DownloadProcess(self, url, IMGLibrary = {}):
        ImgName = url.split('/')[-1]  # [-1]的意思是从网址中最后一个'/'的后一位开始匹配 获取文件名
        ImgID = ImgName[:8]
        headers = {
            'Referer': 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id=' + ImgID,  # Pixiv反爬虫机制
            'User-Agent': 'Mozilla/5.0(Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }
        status = requests.get(url, headers=headers, stream=True).status_code
        chunk_size = 1024
        
        # 通过网页响应返回的状态码来判断是否请求成功 2xx为成功 4xx为客户端错误 3xx为重定向 5xx为服务器错误
        # 404则是访问的页面不存在
        # 403则是被禁止 该程序下说明防盗链不对或爬虫脚本有问题
        # 如果访问正确 则当前图片是jpg 或 png格式的数据 保存为jpg 或 png
        if status != (404 or 403):
            if ImgName in IMGLibrary:   # 如果已经下载图片 则退出函数
                print('The same picture exists!')
                return

            with open('Pixiv_Img/url.txt', 'a') as fp:
                fp.write(ImgName + ':')

            with open('Pixiv_Img/url.txt', 'a') as fp:
                fp.write(str(url) + '\r\n')

            imgsize = requests.get(url, headers=headers).headers['content-length']

            # 显示下载进度条
            ProgressBar = tqdm(
                total=int(imgsize),
                initial=0,
                unit='B',
                unit_scale=True,
                desc=ImgName
            )

            with requests.get(url, headers=headers, stream=True) as img:
                with open('Pixiv_Img/{}.jpg'.format(ImgID), 'wb') as fp:
                    for chunk in img.iter_content(chunk_size=chunk_size):
                        if chunk:
                            fp.write(chunk)
                            ProgressBar.update(chunk_size)
                    ProgressBar.close()

            dict = {ImgName: ImgID}
            IMGLibrary.update(dict)

        if status == (404 or 403):  # 如果jpg格式图片错误 则用png格式保存
            url = url.replace('jpg','png')

            status = requests.get(url, headers=headers, stream=True).status_code
            if status == (404 or 403):  # 如果图片格式不是jpg 和 png 则退出
                print('图片格式不支持下载或者链接被禁止访问!')
                return

            ImgName = url.split('/')[-1]  # [-1]的意思是从网址中最后一个'/'后一位开始匹配 获取文件名
            ImgID = ImgName[:8]    # 截取图片ID
            headers = {
                'Referer': 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id=' + ImgID,  # Pixiv反爬虫机制
                'User-Agent': 'Mozilla/5.0(Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
            }

            if ImgName in IMGLibrary:  # 如果已经下载图片 则退出函数
                print('The same picture exists!')
                return

            with open('Pixiv_Img/url.txt', 'a') as fp:
                fp.write(ImgName + ':')

            with open('Pixiv_Img/url.txt','a') as fp:
                fp.write(str(url) + '\r\n')

            imgsize = requests.get(url, headers=headers).headers['content-length']

            ProgressBar = tqdm(
                total=int(imgsize),
                initial=0,
                unit='B',
                unit_scale=True,
                desc=ImgName
            )

            with requests.get(url, headers=headers, stream=True) as img:
                with open('Pixiv_Img/{}.png' .format(ImgID), 'wb') as fp:
                    for chunk in img.iter_content(chunk_size=chunk_size):
                        if chunk:
                            fp.write(chunk)
                            ProgressBar.update(chunk_size)
                    ProgressBar.close()

            dict = {ImgName:ImgID}
            IMGLibrary.update(dict)

        else:
            return
