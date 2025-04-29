import scrapy


class MercadolivreSpider(scrapy.Spider):
    name = "mercadolivre"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/notebook"]
    page_count = 1
    max_pages = 20

    def parse(self, response):
        products = response.css("div.poly-card__content")

        for product in products:
           
           prices = product.css('span.andes-money-amount__fraction::text').getall()

           yield{
                "brand" : product.css('span.poly-component__brand::text').get(),
                "name" : product.css('a.poly-component__title::text').get(),
                "old_price_reais" : prices[0] if len(prices) > 0 else None,               
                "new_price_reais" : prices[1] if len(prices) > 1 else None, 
                "reviews_rating_number" : product.css('span.poly-reviews__rating::text').get(),        
                "reviews_amount" : product.css('span.poly-reviews__total::text').get(), 
                      
           }
        
        if self.page_count < self.max_pages:
            next_page = response.css('li.andes-pagination__button.andes-pagination__button--next a::attr(href)').get()
            if next_page:
                self.page_count += 1
                yield scrapy.Request(url=next_page, callback=self.parse)

