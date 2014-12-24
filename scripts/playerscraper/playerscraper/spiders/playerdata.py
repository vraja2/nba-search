# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector

from playerscraper.items import PlayerscraperItem


class PlayerdataSpider(CrawlSpider):
    name = 'playerdata'
    allowed_domains = ['basketball-reference.com']
    start_urls = ['http://www.basketball-reference.com/players/']

    rules = (
        Rule(LinkExtractor(allow=r'/players/[a-z]/',restrict_xpaths=('//p',))),
        Rule(LinkExtractor(allow=r'/players/[a-z]/.+\.html'),callback='parse_item')
    )

    def parse_item(self, response):
        sel = Selector(response)
        p = PlayerscraperItem()
        #stores tuples of form ('team_name','year')
        p['teams_played_on'] = [] 
        p['player_name'] = sel.xpath('//h1/text()').extract()[0]   
        for tr in sel.xpath('//table[@id="per_game"]//tr[starts-with(@id,"per_game")]'):
          cols = tr.xpath('.//td')
          year = None
          team = None
          team_link = cols[2].xpath('.//a/text()').extract()
          #don't get year totals for traded players ('TOT'), get individual team information
          #TODO: currently neglecting midseason trades (e.g Rondo traded for Wright, but Rondo's Mavs team includes Wright)
          if team_link: 
            team = team_link[0] 
            year_link = cols[0].xpath('.//a/@href').extract()
            if year_link:
              year = re.search('\d{4}',year_link[0]).group(0)
            else:
              #for old players, in form 1946-47. need to get 47 out and manually add 19
              year_range = cols[0].xpath('.//text()').extract()[0]
              year = "19"+year_range.split('-')[1]
            p['teams_played_on'].append((team,year))
        return p
