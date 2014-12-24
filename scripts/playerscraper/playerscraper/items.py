# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PlayerscraperItem(scrapy.Item):
    # define the fields for your item here like:
    teams_played_on = scrapy.Field()
    player_name = scrapy.Field()
