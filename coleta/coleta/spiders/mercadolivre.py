import scrapy


class MercadolivreSpider(scrapy.Spider):
    name = "mercadolivre"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/notebook"]

    def parse(self, response):
        products = response.css("div.poly-card__content")

        for product in products:
           
           prices = products.css('span.andes-money-amount__fraction::text').getall()

           yield{
                "brand" : product.css('span.poly-component__brand::text').get(),
                "name" : product.css('a.poly-component__title::text').get(),
                "reviews_rating_number" : product.css('span.poly-reviews__rating::text').get(),        
                "reviews_amount" : product.css('span.poly-reviews__total::text').get(), 
                "old_price_reais" : prices[0] if len(prices) > 0 else None,               
                "new_price_reais" : prices[1] if len(prices) > 1 else None,       
           }
