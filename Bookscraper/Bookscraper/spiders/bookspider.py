import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"] #only the domains we want to scrape
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books = response.css("article.product_pod")
        for book in books:

            yield {
                'image':book.css("div.image_container a").attrib['href'],
                'name':book.css("h3 a ::text").get(),
                'book_link':book.css("h3 a").attrib['href']
            }

        next_page_url = response.css("li.next a").attrib['href']
        if next_page_url is not None:
            if 'catalogue/' in next_page_url:
                next_page_url = "https://books.toscrape.com/"+next_page_url
            else:
                next_page_url = "https://books.toscrape.com/catalogue/"+next_page_url
            yield response.follow(next_page_url,callback = self.parse)


