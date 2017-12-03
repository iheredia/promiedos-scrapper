def runspider(dump_dir):
    from scrapy.crawler import CrawlerProcess
    from scrapper.spider import PromiedosSpider

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    PromiedosSpider.dump_dir = dump_dir
    process.crawl(PromiedosSpider)
    process.start()


def runparser(data_dir):
    from scrapper.parser import parse_promedios_data
    parse_promedios_data(data_dir)


if __name__ == '__main__':
    from sys import argv
    import os
    current_dir = os.path.dirname(__file__)
    raw_data_dir = os.path.join(current_dir, 'data/promiedos')

    if '--only-spider' in argv:
        runspider(dump_dir=raw_data_dir)
    elif '--only-parser' in argv:
        runparser(data_dir=raw_data_dir)
    else:
        runspider(dump_dir=raw_data_dir)
        runparser(data_dir=raw_data_dir)
