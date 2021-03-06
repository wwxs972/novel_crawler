# -*- coding: utf-8 -*-
# @Author: Zengjq
# @Date:   2018-09-23 20:12:01
# @Last Modified by:   Zengjq
# @Last Modified time: 2019-03-31 20:01:07
# Scrapy settings for wenku8 project
import os
import platform
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'wenku8'

SPIDER_MODULES = ['wenku8.spiders']
NEWSPIDER_MODULE = 'wenku8.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'wenku8 (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'wenku8.middlewares.Wenku8SpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'wenku8.middlewares.Wenku8DownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'wenku8.pipelines.Wenku8Pipeline': 300,
    'wenku8.pipelines.ImageDownloadPipeline': 300,
}
# 设置图片下载路径
IMAGES_STORE = 'download'
# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Nate's custom settings
# LOG_LEVEL = 'ERROR'  # to only display errors
# LOG_FORMAT = '%(levelname)s: %(message)s'
LOG_FILE = 'log.txt'

# calibre设置
USE_CALIBRE = True
CALIBRE_IP = '192.168.1.6:10012'
CALIBRE_LIBRARY_NAME = '临时书库'
# calibre的用户名密码
CALIBRE_USERNAME = 'ck567'
CALIBRE_PASSWORD = 'ck567'
# 电子书重复是否也添加
ADD_WHEN_DUPLICATE = True

# calibre db
USE_CALIBRE_DB = True
sysstr = platform.system()
if(sysstr == "Windows"):
    CALIBRE_DB_PATH = 'E:/soft/program files/Calibre2_64bit/calibredb.exe'
    CALIBRE_LIBRARY_PATH = 'i:/书库/临时书库/'
elif(sysstr == "Darwin"):
    CALIBRE_DB_PATH = '/Applications/calibre.app/Contents/MacOS/calibredb'
    CALIBRE_LIBRARY_PATH = '~/书库/临时书库/'
else:
    CALIBRE_DB_PATH = ''
    CALIBRE_LIBRARY_PATH = ''
