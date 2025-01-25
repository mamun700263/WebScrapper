import scrapy
from Bookscraper.items import BookscraperItem

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"] #only the domains we want to scrape
    start_urls = ["https://books.toscrape.com"]

    

    def book_detail_parse(self,response):
        table = response.css("table tr")
        book = response.css("div.product_main")[0]
        table_rows = response.css("table tr")
        book_item = BookscraperItem()
        book_item['url'] = response.url
        book_item['title'] = book.css("h1 ::text").get()
        book_item['upc'] = table_rows[0].css("td ::text").get()
        book_item['product_type'] = table_rows[1].css("td ::text").get()
        book_item['price_excl_tax'] = table_rows[2].css("td ::text").get()
        book_item['price_incl_tax'] = table_rows[3].css("td ::text").get()
        book_item['tax'] = table_rows[4].css("td ::text").get()
        book_item['availability'] = table_rows[5].css("td ::text").get()
        book_item['num_reviews'] = table_rows[6].css("td ::text").get()
        book_item['stars'] = book.css("p.star-rating").attrib['class']
        book_item['category'] = book.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get()
        book_item['description'] = book.xpath("//div[@id='product_description']/following-sibling::p/text()").get()
        book_item['price'] = book.css('p.price_color ::text').get()
        yield book_item



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

        next_page_url = response.css("li.next a").attrib['href']
        if next_page_url is not None:
            if 'catalogue/' in next_page_url:
                next_page_url = "https://books.toscrape.com/"+next_page_url
            else:
                next_page_url = "https://books.toscrape.com/catalogue/"+next_page_url
            yield response.follow(next_page_url,callback = self.parse)
            




        

