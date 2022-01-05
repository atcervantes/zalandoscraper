import scrapy
from scrapy import Request

class ZalandoSaleSpider(scrapy.Spider):
    name = 'zalando-sale'
    allowed_domains = ['en.zalando.de']
    start_urls = ['https://en.zalando.de/outlet-mens/']
    base_url = 'https://en.zalando.de'


    def parse(self, response):
        all_products = response.css("article > a::attr(href)").getall()
        
        for product_url in all_products:
            if "outfits" in product_url :
                continue
            yield scrapy.Request(product_url, callback=self.parse_product)
        
        has_next = response.css('._0xLoFW .FCIprz > a:nth-child(3)::attr(href)').get()
        if has_next :
            yield scrapy.Request(
                url = self.base_url + has_next,
                callback = self.parse
            )

    def parse_product(self, response):
        brand = response.css('h3.OEhtt9.ka2E9k.uMhVZi.Kq1JPK.pVrzNP._5Yd-hZ::text').get()
        name = response.css('span.EKabf7.R_QwOV::text').get()
        discount = response.css('span.u-6V88.ka2E9k.uMhVZi.FxZV-M._6yVObe._88STHx.CK43Vi::text').get()
        current_price = response.css('span.uqkIZw.ka2E9k.uMhVZi.dgII7d._6yVObe._88STHx.cMfkVL::text').get()
        normal_price = response.css('span.uqkIZw.ka2E9k.uMhVZi.FxZV-M._6yVObe.weHhRC.ZiDB59::text').get()
        yield {
            'brand' : brand,
            'name' : name,
            'discount' : discount,
            'current_price' : current_price,
            'normal_price' : normal_price,
            'url': response.url
        }