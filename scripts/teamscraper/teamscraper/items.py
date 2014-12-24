# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TeamscraperItem(scrapy.Item):
    # define the fields for your item here like:
    rebound_ranges = scrapy.Field()
    points_ranges = scrapy.Field()
    year = scrapy.Field()
    team = scrapy.Field()
