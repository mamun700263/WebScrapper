import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"] #only the domains we want to scrape
    start_urls = ["https://books.toscrape.com"]
    def book_detail_parse(self,response):
        yield{
        "title ":response.xpath("//div[contains(@class, 'product_main')]/h1/text()").get(),
        "price ":response.xpath("//div[contains(@class, 'product_main')]/p[@class='price_color']/text()").get(),
        "instock" :response.xpath("normalize-space(//p[contains(@class, 'instock availability')])").get(),
        }

    def parse(self, response):
        books = response.css("article.product_pod")
        for book in books:
            detail_page_url = response.css("h3 a").attrib['href']

            if detail_page_url is not None:
                if 'catalogue/' in detail_page_url:
                    detail_page_url = "https://books.toscrape.com/"+detail_page_url
                else:
                    detail_page_url = "https://books.toscrape.com/catalogue/"+detail_page_url
                
                yield response.follow(detail_page_url, callback = self.book_detail_parse)
            image_link = book.css("div.image_container a").attrib['href']
            if image_link is not None:
                if 'catalogue/' in image_link:
                    image_link = "https://books.toscrape.com/"+image_link
                else :
                    image_link = "https://books.toscrape.com/catalogue/"+image_link


            yield {
                'image':image_link,
                'name':book.css("h3 a ::text").get(),
                'book_link':detail_page_url
            }

        next_page_url = response.css("li.next a").attrib['href']
        if next_page_url is not None:
            if 'catalogue/' in next_page_url:
                next_page_url = "https://books.toscrape.com/"+next_page_url
            else:
                next_page_url = "https://books.toscrape.com/catalogue/"+next_page_url
            yield response.follow(next_page_url,callback = self.parse)
            




        

