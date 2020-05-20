# -*- coding: utf-8 -*-
import scrapy

class SpecialOffersSpider(scrapy.Spider):
    name = 'special_offers'
    allowed_domains = ['www.getapp.com/']

    def start_requests(self):
        yield scrapy.Request(url='https://www.getapp.com/project-management-planning-software/a/microsoft-project/reviews', callback=self.parse, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        })

    def parse(self, response):
        for product in response.xpath("//div[@class='listing review-card cd-scope']"):
            yield {
                'title': product.xpath(".//div[@class='incentivized review-origin']/@title").get(),
                'author': response.urljoin(product.xpath(".//div[@class ='review-name']/span/span/text()").get()),
                #'Industry & size': product.xpath(".(//div[@class='industry-title hidden-xs'])/text()").get(),
                # 'original_price': product.xpath(".//div[@class='p_box_price']/span[2]/text()").get(),
                # 'User-Agent': response.request.headers['User-Agent']
            }

        next_page = response.xpath("//a[@data-evla='pagination-button']/@href").get()

        if next_page:
            absolute_url = f"www.getapp.com{next_page}"
            yield scrapy.Request(url=absolute_url, callback=self.parse, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
            })
