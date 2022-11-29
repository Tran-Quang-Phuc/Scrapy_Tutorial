import scrapy
from scrapy.crawler import CrawlerProcess


class newsSpider(scrapy.Spider):
    name = 'news'
    start_urls = ['https://vietnamnet.vn/']

    def parse(self, response):
        all_links = response.xpath('//a/@href').getall()
        for link in all_links:
            if link[-4:] == 'html':
                yield response.follow(link, callback=self.parse_articles)

    def parse_articles(self, response):
        yield {
            'Topic': response.xpath('//div[@class="breadcrumb-box__link "]/p/a[1]/@title').get(),
            'Category': response.xpath('//div[@class="breadcrumb-box__link "]/p/a[2]/@title').get(),
            'Title': response.xpath('//h1/text()').get(),
            'Url': response.url,
            'Author': response.xpath('//p[@class="newsFeature__author-info"]/span[1]/a/@title').get(),
        }


if __name__ == "__main__":
    newsCrawler = CrawlerProcess()
    newsCrawler.crawl(newsSpider)
    newsCrawler.start()
