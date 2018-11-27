import scrapy
#from recipes.items import RecipesItem
from scrapy import Request

class RecipesSpider(scrapy.Spider):
    name = "recipes"

    allowed_domains = ['tasty.co']
    start_urls = ['https://tasty.co/compilation/tasty-noodle-recipes']


    def parse(self, response):
        categories = response.xpath('//body/div[@class="xs-flex-grow-1"]/div[@class="content-wrap search-wrap clearfix xs-mx-auto xs-px2"]/div[@class="xs-block-grid-2 sm-block-grid-4"]/a')
        for linktocategory in categories:
            link = linktocategory.xpath('@href').extract_first()
            yield scrapy.Request(link, callback=self.parse_Category)
    
    def parse_Category(self, response):
        allrecipes_list = response.xpath('//body/div[@class="content-wrap xs-flex-grow-1 clearfix xs-mx-auto xs-col-12"]/section[@class="compilation-recipes xs-mt2"]/div[@class="compilation-recipes__list xs-m1 lg-m1 xs-mb4 lg-mb4 lg-mb5 xs-block-grid-2 lg-block-grid-4"]/a')
        for linktorecipe in allrecipes_list:
            url = linktorecipe.xpath('@href').extract_first()
            title = linktorecipe.xpath('div/h6/text()').extract_first()
            yield scrapy.Request(url, callback=self.parse_Recipe, meta={'URL': url, 'Title': title})

    def parse_Recipe(self, response):
        self.logger.info("Visited %s", response.url)
        url = response.meta.get('URL')
        title = response.meta.get('Title')

        content = "".join(line for line in response.xpath('//script[@type="application/ld+json"]/text()').extract_first())

        yield{'URL': url, 'Title': title, 'Content': content}
