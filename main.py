from scrapy.crawler import CrawlerProcess
from scrapper.spider import PromiedosSpider

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(PromiedosSpider)
process.start()
