import scrapy
from scrapy.crawler import CrawlerProcess


class VnexpressSpider(scrapy.Spider):
    name = 'vnexpress'
    allowed_domains = ['vnexpress.net']
    start_urls = ['https://vnexpress.net/']

    def parse(self, response):
        article_links = response.xpath('//article//a/@href')[1:-1]
        for link in article_links:
            yield response.follow(link.get(), callback=self.parse_articles)

        topics = response.xpath('//ul[@class="parent"]/li')
        for topic in topics:
            topic_name = topic.xpath('./@class').get()
            topic_link = topic.xpath('./a/@href')
            if topic_name == 'newlest':
                yield response.follow(topic_link.get(), callback=self.parse_categories)
            elif topic_name == 'gocnhin':
                pass
            elif topic_name == 'video':
                pass
            elif topic_name == 'podcasts':
                pass
            else:
                yield response.follow(topic_link.get(), callback=self.parse_topics)

    def parse_topics(self, response):
        article_links = response.xpath('//article//a/@href')
        for link in article_links:
            yield response.follow(link.get(), callback=self.parse_articles)

        categories = response.xpath('//ul[@class="ul-nav-folder"]/li/a/@href')
        for category in categories:
            yield response.follow(category.get(), callback=self.parse_categories)

    def parse_categories(self, response):
        article_links = response.xpath('//article//a/@href')
        for article in article_links:
            yield response.follow(article.get(), callback=self.parse_articles)
            
    def parse_articles(self, response):
        yield {
            'Topic': response.xpath('//ul[@class="breadcrumb"]/li/a/text()').get(),
            'Category': response.xpath('//ul[@class="breadcrumb"]/li[2]/a/text()').get(),
            'Title': response.xpath('//h1/text()').get(),
            'Url': response.url,
            'Author': response.xpath('//p/strong/text()').get(),
            'Date': response.xpath('//span[@class="date"]/text()').get()
        }


if __name__ == '__main__':
    crawler = CrawlerProcess()
    crawler.crawl(VnexpressSpider)
    crawler.start()
