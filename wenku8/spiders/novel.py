# -*- coding: utf-8 -*-
# @Author: Zengjq
# @Date:   2018-09-23 09:18:38
# @Last Modified by:   Zengjq
# @Last Modified time: 2019-03-31 19:35:26
import os
import scrapy
from wenku8.items import ChapterItem, VolumnItem, ImageItem
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc
from bs4 import BeautifulSoup


class NovelSpider(scrapy.Spider):
    name = 'novel'
    save_path = 'download'
    # allowed_domains = ['www.wenku8.net', 'pic.wkcdn.com']

    @staticmethod
    def name_filter(title):
        # 小说名称里面的大圆点号 KATAKANA MIDDLE DOT
        title = title.replace(u'\u30fb', ' ').strip()
        return title

    @staticmethod
    def content_filter(content):
        replace_word_list = [u'\r\n', u'\xa0']
        for replace_word in replace_word_list:
            content = content.replace(replace_word, ' ')
        return content

    def start_requests(self):
        novel_no = getattr(self, 'no', None)
        if novel_no != None:
            url = 'https://www.wenku8.net/book/%s.htm' % novel_no
        else:
            url = 'https://www.wenku8.net/book/1213.htm'
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        """
        小说首页解析
        scrapy shell https://www.wenku8.net/book/1618.htm
        scrapy shell https://www.wenku8.net/book/1715.htm
        """
        # 小说名称
        novel_name = response.css("#content > div:nth-child(1) > table:nth-child(1) > tr:nth-child(1) > td > table > tr > td:nth-child(1) > span > b::text").extract_first().strip()
        # 作者
        novel_author = response.css("#content > div:nth-child(1) > table:nth-child(1) > tr:nth-child(2) > td:nth-child(2)::text").extract_first()[5:].strip()
        # 封面图(仅在没有更好的图片的时候才用)
        novel_cover = response.css("#content > div:nth-child(1) > table:nth-child(4) > tr > td:nth-child(1) > img::attr(src)").extract_first()
        # 小说简介
        novel_description = ''.join(response.css("#content > div:nth-child(1) > table:nth-child(4) > tr > td:nth-child(2) > span:nth-child(11)::text").extract())

        novel_info = {}
        novel_no = response.url.split('/')[-1].split('.')[0]
        novel_info['novel_no'] = novel_no
        novel_info['novel_name'] = novel_name
        novel_info['novel_author'] = novel_author
        novel_info['novel_cover'] = novel_cover
        novel_info['novel_description'] = novel_description

        # 目录页面链接
        index_url = response.css("#content > div:nth-child(1) > div:nth-child(6) > div > span:nth-child(1) > fieldset > div > a::attr(href)").extract_first()

        # 获取目录页面
        yield scrapy.Request(index_url, meta={'novel_info': novel_info}, callback=self.parse_index)

    def parse_index(self, response):
        """
        目录解析
        scrapy shell https://www.wenku8.net/novel/1/1618/index.htm
        """
        # volumns = response.css(".vcss")
        # chapters = response.css(".ccss")
        novel_info = response.meta['novel_info']
        novel_no = novel_info['novel_no']

        # 由于网站的卷名称和章节属于同一级关系 这里要做解析
        tds = response.css("body > table td")
        volumns = []
        # 初始化单卷的信息数据
        volumn = {'volumn_name': '', 'chapters': [], 'images': []}
        chapters = []
        current_volumn_count = 0
        current_chapter_count = 0
        # 获取当前请求的url 用于处理相对路径
        base_url = get_base_url(response)
        # print('base_url', base_url)
        for td in tds:
            td_class = td.css("::attr(class)").extract_first()

            # 一卷
            if td_class == 'vcss':
                if volumn['volumn_name'] != '':
                    # 卷名不为空 说明上一卷的所有章节都解析完了 要先把上一卷的信息存起来
                    volumn['chapters'] = chapters
                    volumns.append(volumn)
                    # 初始化现在要解析的这一卷数据
                    volumn = {'volumn_name': '', 'chapters': [], 'images': []}
                    chapters = []
                    # 重置章节数
                    current_chapter_count = 0
                    # 卷数加一
                    current_volumn_count += 1
                # 每卷的标题
                volumn_name = td.css("::text").extract_first()
                volumn['volumn_name'] = volumn_name

            # 一章
            if td_class == 'ccss':
                # 获取章节名称
                chapter_name = td.css("::text").extract_first()
                # 名称过滤
                chapter_name = self.name_filter(chapter_name)
                if chapter_name == '':
                    # 空的章节 跳过
                    continue
                else:
                    # 有内容的章节
                    # print chapter_name
                    chapter_relative_link = td.css("::attr(href)").extract_first()
                    # 处理相对路径
                    chapter_link = urljoin_rfc(base_url, chapter_relative_link)
                    chapters.append([chapter_name, chapter_link])
        # 最后一个卷解析结束 手动把cahpter存入volumn 再把最后一个volumn存入volumns
        volumn['chapters'] = chapters
        volumns.append(volumn)

        # 开始发送请求 获取各卷的每个章节的页面
        print('总卷数 %s' % len(volumns))
        for index, volumn in enumerate(volumns):
            chapter_index = 0
            print(index, volumn['volumn_name'], str(volumn['chapters'][chapter_index][1], 'utf-8'))
            yield scrapy.Request(str(volumn['chapters'][chapter_index][1], 'utf-8'), meta={'novel_info': novel_info, 'volumn': volumn, 'chapter_index': chapter_index, 'volumn_index': index}, callback=self.parse_chapter)

    def parse_chapter(self, response):
        """
        页面解析
        scrapy shell https://www.wenku8.net/novel/1/1618/54879.htm
        """
        novel_info = response.meta['novel_info']
        volumn = response.meta['volumn']
        chapter_index = response.meta['chapter_index']
        volumn_index = response.meta['volumn_index']
        novel_no = novel_info['novel_no']
        images = volumn['images']

        # 内容
        chapter_content = response.css("#content").extract_first()
        chapter_content = self.content_filter(chapter_content)

        # 提取图片url 并改写
        soup_detail = BeautifulSoup(chapter_content, "lxml", from_encoding='utf-8')
        # 提取包含图片的div
        image_divs = soup_detail.find_all('div', class_='divimage')
        # 提取图片链接
        for image_div in image_divs:
            # 提取子元素 插入到和父级元素同级的位置
            image_div.insert(0, image_div.a.img)
            # 删除不需要的元素
            image_div.a.extract()
            # 提取图片路径
            image_url = image_div.img.get('src')
            images.append(image_url)
            # 修改为相对路径
            image_div.img['src'] = '../Images/' + image_url.split('/')[-1]

        # 保存图片链接
        volumn['images'] = images

        # 把修改后的页面存回去
        chapter_content = soup_detail.prettify()

        # dirty hack
        # 因为使用ebooklib生成epub可以直接用数据 不用文件 这里就省掉生成单个文件的步骤
        # chapter_item = ChapterItem()
        # chapter_item['volumn_index'] = volumn_index
        # chapter_item['chapter_index'] = chapter_index
        # chapter_item['chapter_content'] = chapter_content
        # chapter_item['novel_no'] = novel_no
        # yield chapter_item

        # 直接把每个章节的内容写到volumn里面
        volumn['chapters'][chapter_index].append(chapter_content)
        if len(volumn['chapters']) != chapter_index + 1:
            chapter_index += 1
            yield scrapy.Request(str(volumn['chapters'][chapter_index][1], 'utf-8'), meta={'novel_info': novel_info, 'volumn': volumn, 'chapter_index': chapter_index, 'volumn_index': volumn_index}, callback=self.parse_chapter)

        else:
            # 卷 item
            volumn_item = VolumnItem()
            volumn_item['novel_info'] = novel_info
            volumn_item['volumn'] = volumn
            volumn_item['volumn_index'] = volumn_index
            # yield volumn_item

            # 已经遍历完所有的章节 接下来要把图片下载下来
            image_item = ImageItem()
            image_item['image_urls'] = volumn['images']
            image_item['volumn_item'] = volumn_item
            # image_item['novel_no'] = novel_info['novel_no']
            image_item['download_finish_flag'] = False
            yield image_item
