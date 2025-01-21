import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"] #only the domains we want to scrape
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        pass
