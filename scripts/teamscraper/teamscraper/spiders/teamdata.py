# -*- coding: utf-8 -*-
import scrapy
import urlparse
import re
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from teamscraper.items import TeamscraperItem

class TeamdataSpider(CrawlSpider):
    name = 'teamdata'
    allowed_domains = ['basketball-reference.com']
    start_urls = ['http://www.basketball-reference.com/teams/']

    rules = (
        Rule(LinkExtractor(allow=r'/teams/.+',restrict_xpaths=('//table[@id="active"]',))),
        Rule(LinkExtractor(allow=r'/teams/.+/\d{4}\.html'),callback="parse_item")
    )

    def parse_item(self, response):
        sel = Selector(response)
        url = response.url
        #of the form "teams/team_name/year.html"
        path = urlparse.urlparse(url).path
        year = re.search('\d{4}',path).group(0)
        team_name = path.split('/')[2] 
        t = TeamscraperItem()
        t['team'] = team_name
        t['year'] = year
        #[0-5]->0, [6-10]->1, [11-15]->2, [16-20]->3, [21+]->4
        t['rebound_ranges'] = [set() for i in range(5)]
        #[0-5]->0, [6-10]->1, [11-15]->2, [16-20]->3, [21-25]->4, [26-30]->5, [30-35]->6, [36+]->7
        t['points_ranges'] = [set() for i in range(8)]
        for tr in sel.xpath('//table[@id="per_game"]//tr')[1:]:
          cols = tr.xpath('.//td')
          player_name_l = cols[1].xpath('.//a/text()').extract()
          rebounds_pgame_l = cols[20].xpath('.//text()').extract()
          points_pgame_l = cols[26].xpath('.//text()').extract()
          if player_name_l and rebounds_pgame_l and points_pgame_l:
            player_name = player_name_l[0]
            rebounds_pgame = float(rebounds_pgame_l[0])
            points_pgame = float(points_pgame_l[0])
            #categorize 
            if rebounds_pgame <= 5:
              t['rebound_ranges'][0].add(player_name)
            elif rebounds_pgame <= 10:
              t['rebound_ranges'][1].add(player_name)
            elif rebounds_pgame <= 15:
              t['rebound_ranges'][2].add(player_name)
            elif rebounds_pgame <= 20:
              t['rebound_ranges'][3].add(player_name)
            else:
              t['rebound_ranges'][4].add(player_name)
            if points_pgame <= 5:
              t['points_ranges'][0].add(player_name)
            elif points_pgame <= 10:
              t['points_ranges'][1].add(player_name)
            elif points_pgame <= 15:
              t['points_ranges'][2].add(player_name)
            elif points_pgame <= 20:
              t['points_ranges'][3].add(player_name)
            elif points_pgame <= 25:
              t['points_ranges'][4].add(player_name)
            elif points_pgame <= 30:
              t['points_ranges'][5].add(player_name)
            elif points_pgame <= 35:
              t['points_ranges'][6].add(player_name)
            else:
              t['points_ranges'][7].add(player_name)
        return t
