# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector

from playerdatascraper.items import PlayerdatascraperItem

def get_int_val(val):
  return int(val) if val else val

def get_float_val(val):
  return float(val) if val else val

def remove_percent_get_float(percent_val):
  val = None
  if percent_val:
    percent_list = percent_val.split("%")
    val = percent_list[0]
  return get_float_val(val)

def initialize_per100_none(player_data):
  player_data['per_100_FGM'] = None
  player_data['per_100_FGA'] = None
  player_data['per_100_3P_FGM'] = None
  player_data['per_100_3P_FGA'] = None
  player_data['per_100_2P_FGM'] = None
  player_data['per_100_2P_FGA'] = None
  player_data['per_100_FTM'] = None
  player_data['per_100_FTA'] = None
  player_data['per_100_ORB'] = None
  player_data['per_100_DRB'] = None
  player_data['per_100_TRB'] = None
  player_data['per_100_AST'] = None
  player_data['per_100_STL'] = None
  player_data['per_100_BLK'] = None
  player_data['per_100_TOV'] = None
  player_data['per_100_PF'] = None
  player_data['per_100_PTS'] = None
  player_data['per_100_ORTG'] = None
  player_data['per_100_DRTG'] = None

def initialize_shooting_none(player_data):
  player_data['shooting_dist'] = None
  player_data['shooting_percent_2P'] = None
  player_data['shooting_percent_0_3'] = None
  player_data['shooting_percent_3_10'] = None
  player_data['shooting_percent_10_16'] = None
  player_data['shooting_percent_16_l3'] = None
  player_data['shooting_percent_3P'] = None
  player_data['shooting_FG_percent_0_3'] = None
  player_data['shooting_FG_percent_3_10'] = None
  player_data['shooting_FG_percent_16_l3'] = None
  player_data['shooting_percent_ast_2P'] = None
  player_data['shooting_percent_FG_dunks'] = None
  player_data['shooting_made_dunks'] = None
  player_data['shooting_percent_ast_3P'] = None
  player_data['shooting_percent_3P_corner'] = None
  player_data['shooting_FG_percent_3P_corner'] = None

def initialize_pbp_none(player_data):
  player_data['pbp_PG_percent'] = None
  player_data['pbp_SG_percent'] = None
  player_data['pbp_SF_percent'] = None
  player_data['pbp_PF_percent'] = None
  player_data['pbp_C_percent'] = None
  player_data['pbp_plusminus_oncourt'] = None 
  player_data['pbp_plusminus_onoff'] = None 
  player_data['pbp_TOV_badpass'] = None 
  player_data['pbp_TOV_lostball'] = None 
  player_data['pbp_TOV_other'] = None 
  player_data['pbp_PGA'] = None
  player_data['pbp_Sfdrawn'] = None
  player_data['pbp_And1']= None
  player_data['pbp_FGA_blocked'] = None

class PlayerdataspiderSpider(CrawlSpider):
    name = 'playerdataspider'
    allowed_domains = ['basketball-reference.com']
    start_urls = ['http://www.basketball-reference.com/players/']

    rules = (
        Rule(LinkExtractor(allow=r'/[a-z]/$'), follow=True),
        Rule(LinkExtractor(allow=r'/[a-z]/\w+\.html$'), callback='parse_item'),
    ) 

    def parse_item(self, response):
        url = response.url
        sel = Selector(response)
        curr_year = 2016
        
        name = sel.xpath('//h1/text()').extract()[0]
        
        id_start_idx = re.search(r"/\w+\.html",url).start() 
        id_end_idx = re.search(r"/\w+\.html",url).end() 
        id = url[id_start_idx+1:id_end_idx-5]

        birthday = sel.xpath('//span[@id="necro-birth"]/@data-birth').extract()
        curr_age = None
        if birthday:
          birthday_list = birthday[0].split('-')
          birth_year = int(birthday_list[0])
          birth_month = int(birthday_list[1])
          birth_date = int(birthday_list[2])
          curr_age = curr_year-birth_year
        
        totals_data_rows = sel.xpath('//table[@id="totals"]//tr[@class="full_table"]')
        per_game_rows = sel.xpath('//table[@id="per_game"]//tr[@class="full_table"]')
        player_data_objs = []
        for row in totals_data_rows:
          totals_data_cols = row.xpath('td')
          player_data = PlayerdatascraperItem()
          player_data['name'] = name
          age = totals_data_cols[1].xpath('text()').extract_first()
          player_data['age'] = int(age) if age else age
          player_data['team'] = totals_data_cols[2].xpath('a/text()').extract_first()
          player_data['league'] = totals_data_cols[3].xpath('a/text()').extract_first()
          
          # could be unfilled
          player_data['position'] = totals_data_cols[4].xpath('text()').extract_first()
          
          games_played = totals_data_cols[5].xpath('text()').extract_first()
          player_data['games_played'] = int(games_played) if games_played else games_played
          games_started = totals_data_cols[6].xpath('text()').extract_first()
          player_data['games_started'] = int(games_started) if games_started else games_started
          
          total_MP = totals_data_cols[7].xpath('text()').extract_first()
          player_data['total_MP'] = int(total_MP) if total_MP else total_MP
          player_data['total_FGM'] = int(totals_data_cols[8].xpath('text()').extract_first())
          player_data['total_FGA'] = int(totals_data_cols[9].xpath('text()').extract_first())
          
          FG_percent = totals_data_cols[10].xpath('text()').extract_first()
          player_data['FG_percent'] = float(FG_percent) if FG_percent else FG_percent
          
          total_3P_FGM = totals_data_cols[11].xpath('text()').extract_first()
          player_data['total_3P_FGM'] = int(total_3P_FGM) if total_3P_FGM else total_3P_FGM
          total_3P_FGA = totals_data_cols[12].xpath('text()').extract_first()
          player_data['total_3P_FGA'] = int(total_3P_FGA) if total_3P_FGA else total_3P_FGA

          three_P_percent = totals_data_cols[13].xpath('text()').extract_first()
          player_data['three_P_percent'] = float(three_P_percent) if three_P_percent else three_P_percent

          player_data['total_2P_FGM'] = int(totals_data_cols[14].xpath('text()').extract_first())
          player_data['total_2P_FGA'] = int(totals_data_cols[15].xpath('text()').extract_first())
          
          two_P_percent = totals_data_cols[16].xpath('text()').extract_first() 
          player_data['two_P_percent'] = float(two_P_percent) if two_P_percent else two_P_percent
          player_data['eFG_percent'] = float(totals_data_cols[17].xpath('text()').extract_first())

          player_data['total_FTM'] = int(totals_data_cols[18].xpath('text()').extract_first())
          player_data['total_FTA'] = int(totals_data_cols[19].xpath('text()').extract_first())
          FT_percent = totals_data_cols[20].xpath('text()').extract_first()
          player_data['FT_percent'] = float(FT_percent) if FT_percent else FT_percent

          total_ORB = totals_data_cols[21].xpath('text()').extract_first()
          player_data['total_ORB'] = int(total_ORB) if total_ORB else total_ORB
          total_DRB = totals_data_cols[22].xpath('text()').extract_first()
          player_data['total_DRB'] = int(total_DRB) if total_DRB else total_DRB
          total_TRB = totals_data_cols[23].xpath('text()').extract_first()
          player_data['total_TRB'] = int(total_TRB) if total_TRB else total_TRB
          
          player_data['total_AST'] = int(totals_data_cols[24].xpath('text()').extract_first())
          
          total_STL = totals_data_cols[25].xpath('text()').extract_first()
          player_data['total_STL'] = int(total_STL) if total_STL else total_STL
          
          total_BLK = totals_data_cols[26].xpath('text()').extract_first()
          player_data['total_BLK'] = int(total_BLK) if total_BLK else total_BLK

          total_TOV = totals_data_cols[27].xpath('text()').extract_first()
          player_data['total_TOV'] = int(total_TOV) if total_TOV else total_TOV
          
          player_data['total_PF'] = int(totals_data_cols[28].xpath('text()').extract_first())
          player_data['total_PTS'] = int(totals_data_cols[29].xpath('text()').extract_first())
          player_data_objs.append(player_data)

        per_game_rows = sel.xpath('//table[@id="per_game"]//tr[@class="full_table"]')
        for k,row in enumerate(per_game_rows):
          per_game_cols = row.xpath('td')
          player_data = player_data_objs[k]
          per_game_MP = per_game_cols[7].xpath('text()').extract_first()
          player_data['per_game_MP'] = float(per_game_MP) if per_game_MP else per_game_MP
          player_data['per_game_FGM'] = per_game_cols[8].xpath('text()').extract_first()
          player_data['per_game_FGA'] = per_game_cols[9].xpath('text()').extract_first()

          per_game_3P_FGM = per_game_cols[11].xpath('text()').extract_first()
          player_data['per_game_3P_FGM'] = float(per_game_3P_FGM) if per_game_3P_FGM else per_game_3P_FGM
          per_game_3P_FGA = per_game_cols[12].xpath('text()').extract_first()
          player_data['per_game_3P_FGA'] = float(per_game_3P_FGA) if per_game_3P_FGA else per_game_3P_FGA
          
          player_data['per_game_2P_FGM'] = float(per_game_cols[14].xpath('text()').extract_first())
          player_data['per_game_2P_FGA'] = float(per_game_cols[15].xpath('text()').extract_first())

          player_data['per_game_FTM'] = float(per_game_cols[18].xpath('text()').extract_first())
          player_data['per_game_FTA'] = float(per_game_cols[19].xpath('text()').extract_first())
          
          per_game_ORB = per_game_cols[21].xpath('text()').extract_first()
          player_data['per_game_ORB'] = float(per_game_ORB) if per_game_ORB else per_game_ORB
          per_game_DRB = per_game_cols[22].xpath('text()').extract_first()
          player_data['per_game_DRB'] = float(per_game_DRB) if per_game_DRB else per_game_DRB
          per_game_TRB = per_game_cols[23].xpath('text()').extract_first()
          player_data['per_game_TRB'] = float(per_game_TRB) if per_game_TRB else per_game_TRB 
          
          player_data['per_game_AST'] = float(per_game_cols[24].xpath('text()').extract_first())
          per_game_STL = per_game_cols[25].xpath('text()').extract_first()
          player_data['per_game_STL'] = float(per_game_STL) if per_game_STL else per_game_STL
          per_game_BLK = per_game_cols[26].xpath('text()').extract_first()
          player_data['per_game_BLK'] = float(per_game_BLK) if per_game_BLK else per_game_BLK
          per_game_TOV = per_game_cols[27].xpath('text()').extract_first()
          player_data['per_game_TOV'] = float(per_game_TOV) if per_game_TOV else per_game_TOV
          
          player_data['per_game_PF'] = float(per_game_cols[28].xpath('text()').extract_first())
          player_data['per_game_PTS'] = float(per_game_cols[29].xpath('text()').extract_first())

        per_36_rows = sel.xpath('//table[@id="per_minute"]//tr[@class="full_table"]')
        for k,row in enumerate(per_36_rows):
          per_36_cols = row.xpath('td')
          player_data = player_data_objs[k]
          per_36_FGM = per_36_cols[8].xpath('text()').extract_first()
          player_data['per_36_FGM'] = float(per_36_FGM) if per_36_FGM else per_36_FGM
          per_36_FGA = per_36_cols[9].xpath('text()').extract_first()
          player_data['per_36_FGA'] = float(per_36_FGA) if per_36_FGA else per_36_FGA
          per_36_3P_FGM = per_36_cols[11].xpath('text()').extract_first()
          player_data['per_36_3P_FGM'] = float(per_36_3P_FGM) if per_36_3P_FGM else per_36_3P_FGM
          per_36_3P_FGA = per_36_cols[12].xpath('text()').extract_first()
          player_data['per_36_3P_FGA'] = float(per_36_3P_FGA) if per_36_3P_FGA else per_36_3P_FGA
          per_36_2P_FGM = per_36_cols[14].xpath('text()').extract_first()
          player_data['per_36_2P_FGM'] = float(per_36_2P_FGM) if per_36_2P_FGM else per_36_2P_FGM
          per_36_2P_FGA = per_36_cols[15].xpath('text()').extract_first()
          player_data['per_36_2P_FGA'] = float(per_36_2P_FGA) if per_36_2P_FGA else per_36_2P_FGA
          per_36_FTM = per_36_cols[17].xpath('text()').extract_first()
          player_data['per_36_FTM'] = get_float_val(per_36_FTM)
          per_36_FTA = per_36_cols[18].xpath('text()').extract_first()
          player_data['per_36_FTA'] = get_float_val(per_36_FTA) 
          per_36_ORB = per_36_cols[20].xpath('text()').extract_first()
          player_data['per_36_ORB'] = get_float_val(per_36_ORB)
          per_36_DRB = per_36_cols[21].xpath('text()').extract_first()
          player_data['per_36_DRB'] = get_float_val(per_36_DRB)
          per_36_TRB = per_36_cols[22].xpath('text()').extract_first()
          player_data['per_36_TRB'] = get_float_val(per_36_TRB)
          per_36_AST = per_36_cols[23].xpath('text()').extract_first()
          player_data['per_36_AST'] = get_float_val(per_36_AST)
          per_36_STL = per_36_cols[24].xpath('text()').extract_first()
          player_data['per_36_STL'] = get_float_val(per_36_STL)
          per_36_BLK = per_36_cols[25].xpath('text()').extract_first()
          player_data['per_36_BLK'] = get_float_val(per_36_BLK)
          per_36_TOV = per_36_cols[26].xpath('text()').extract_first()
          player_data['per_36_TOV'] = get_float_val(per_36_TOV)
          per_36_PF = per_36_cols[27].xpath('text()').extract_first()
          player_data['per_36_PF'] = get_float_val(per_36_PF)
          per_36_PTS = per_36_cols[28].xpath('text()').extract_first()
          player_data['per_36_PTS'] = get_float_val(per_36_PTS)
          
        
        per_100_rows =  sel.xpath('//table[@id="per_poss"]//tr[@class="full_table"]')
        if per_100_rows:
          offset = 0
          if len(per_100_rows) != len(per_game_rows):
            offset = len(per_game_rows) - len(per_100_rows)
          if offset != 0:
            for i in range(offset):
              initialize_per100_none(player_data_objs[i])
          for k,row in enumerate(per_100_rows):
            per_100_cols = row.xpath('td')
            player_data = player_data_objs[k+offset]
            per_100_FGM = per_100_cols[8].xpath('text()').extract_first()
            player_data['per_100_FGM'] = get_float_val(per_100_FGM)
            
            per_100_FGA = per_100_cols[9].xpath('text()').extract_first()
            player_data['per_100_FGA'] = get_float_val(per_100_FGA)
            
            per_100_3P_FGM =  per_100_cols[11].xpath('text()').extract_first()
            player_data['per_100_3P_FGM'] = get_float_val(per_100_3P_FGM)
            
            per_100_3P_FGA =  per_100_cols[12].xpath('text()').extract_first()
            player_data['per_100_3P_FGA'] = get_float_val(per_100_3P_FGA)
            
            per_100_2P_FGM = per_100_cols[14].xpath('text()').extract_first()
            player_data['per_100_2P_FGA'] = get_float_val(per_100_3P_FGA)
            
            per_100_2P_FGA = per_100_cols[15].xpath('text()').extract_first()
            player_data['per_100_2P_FGA'] = get_float_val(per_100_2P_FGA)

            per_100_FTM = per_100_cols[17].xpath('text()').extract_first()
            player_data['per_100_FTM'] = get_float_val(per_100_FTM)

            per_100_FTA = per_100_cols[18].xpath('text()').extract_first()
            player_data['per_100_FTA'] = get_float_val(per_100_FTA) 
            
            per_100_ORB = per_100_cols[20].xpath('text()').extract_first()
            player_data['per_100_ORB'] = get_float_val(per_100_ORB)
            
            per_100_DRB = per_100_cols[21].xpath('text()').extract_first()
            player_data['per_100_DRB'] = get_float_val(per_100_DRB)
            
            per_100_TRB = per_100_cols[22].xpath('text()').extract_first()
            player_data['per_100_TRB'] = get_float_val(per_100_TRB)
            
            per_100_AST = per_100_cols[23].xpath('text()').extract_first()
            player_data['per_100_AST'] = get_float_val(per_100_AST)
            
            per_100_STL = per_100_cols[24].xpath('text()').extract_first()
            player_data['per_100_STL'] = get_float_val(per_100_STL)
            
            per_100_BLK = per_100_cols[25].xpath('text()').extract_first()
            player_data['per_100_BLK'] = get_float_val(per_100_BLK)
            
            per_100_TOV = per_100_cols[26].xpath('text()').extract_first()
            player_data['per_100_TOV'] = get_float_val(per_100_TOV)
            
            per_100_PF = per_100_cols[27].xpath('text()').extract_first()
            player_data['per_100_PF'] = get_float_val(per_100_PF)
            
            per_100_PTS = per_100_cols[28].xpath('text()').extract_first()
            player_data['per_100_PTS'] = get_float_val(per_100_PTS)
            
            per_100_ORTG = per_100_cols[30].xpath('text()').extract_first()
            player_data['per_100_ORTG'] = get_float_val(per_100_ORTG)

            per_100_DRTG = per_100_cols[31].xpath('text()').extract_first()
            player_data['per_100_DRTG'] = get_float_val(per_100_DRTG)

        else:
          for player_data in player_data_objs:
            initialize_per100_none(player_data)

        advanced_rows =  sel.xpath('//table[@id="advanced"]//tr[@class="full_table"]')
        for k,row in enumerate(advanced_rows):
          advanced_cols = row.xpath('td')
          player_data = player_data_objs[k]
          
          advanced_PER = advanced_cols[7].xpath('text()').extract_first()
          player_data['advanced_PER'] = get_float_val(advanced_PER)

          advanced_TS_percent = advanced_cols[8].xpath('text()').extract_first()
          player_data['advanced_TS_percent'] = get_float_val(advanced_TS_percent)

          advanced_3PAR = advanced_cols[9].xpath('text()').extract_first()
          player_data['advanced_3PAR'] = get_float_val(advanced_3PAR)

          advanced_FTR = advanced_cols[10].xpath('text()').extract_first()
          player_data['advanced_FTR'] = get_float_val(advanced_FTR)

          advanced_ORB_percent = advanced_cols[11].xpath('text()').extract_first()
          player_data['advanced_ORB_percent'] = get_float_val(advanced_ORB_percent)

          advanced_DRB_percent = advanced_cols[12].xpath('text()').extract_first()
          player_data['advanced_DRB_percent'] = get_float_val(advanced_DRB_percent)

          advanced_TRB_percent = advanced_cols[13].xpath('text()').extract_first()
          player_data['advanced_TRB_percent'] = get_float_val(advanced_TRB_percent)

          advanced_AST_percent = advanced_cols[14].xpath('text()').extract_first()
          player_data['advanced_AST_percent'] = get_float_val(advanced_AST_percent)
   
          advanced_STL_percent = advanced_cols[15].xpath('text()').extract_first()
          player_data['advanced_STL_percent'] = get_float_val(advanced_STL_percent)
    
          advanced_BLK_percent = advanced_cols[16].xpath('text()').extract_first()
          player_data['advanced_BLK_percent'] = get_float_val(advanced_BLK_percent)
    
          advanced_TOV_percent = advanced_cols[17].xpath('text()').extract_first()
          player_data['advanced_TOV_percent'] = get_float_val(advanced_TOV_percent)
   
          advanced_USG_percent = advanced_cols[18].xpath('text()').extract_first()
          player_data['advanced_USG_percent'] = get_float_val(advanced_USG_percent)

          advanced_OWS = advanced_cols[20].xpath('text()').extract_first()
          player_data['advanced_OWS'] = get_float_val(advanced_OWS)
    
          advanced_DWS = advanced_cols[21].xpath('text()').extract_first()
          player_data['advanced_DWS'] = get_float_val(advanced_DWS)

          advanced_WS = advanced_cols[22].xpath('text()').extract_first()
          player_data['advanced_WS'] = get_float_val(advanced_WS)

          advanced_WS48 = advanced_cols[23].xpath('text()').extract_first()
          player_data['advanced_WS48'] = get_float_val(advanced_WS48)

          advanced_OBPM = advanced_cols[25].xpath('text()').extract_first()
          player_data['advanced_OBPM'] = get_float_val(advanced_OBPM)
          
          advanced_DBPM = advanced_cols[26].xpath('text()').extract_first()
          player_data['advanced_DBPM'] = get_float_val(advanced_DBPM)
    
          advanced_BPM = advanced_cols[27].xpath('text()').extract_first()
          player_data['advanced_BPM'] = get_float_val(advanced_BPM)
    
          advanced_VORP = advanced_cols[28].xpath('text()').extract_first()
          player_data['advanced_VORP'] = get_float_val(advanced_VORP)

        
        shooting_rows = sel.xpath('//table[@id="shooting"]//tr[@class="full_table"]')
        if shooting_rows:
          offset = 0
          if len(shooting_rows) != len(per_game_rows):
            offset = len(per_game_rows) - len(shooting_rows)
          if offset != 0:
            for i in range(offset):
              initialize_shooting_none(player_data_objs[i])
          for k,row in enumerate(shooting_rows):
            shooting_cols = row.xpath('td')
            player_data = player_data_objs[k+offset]

            shooting_dist = shooting_cols[8].xpath('text()').extract_first()
            player_data['shooting_dist'] = get_float_val(shooting_dist)
            
            shooting_percent_2P = shooting_cols[9].xpath('text()').extract_first()
            player_data['shooting_percent_2P'] = get_float_val(shooting_percent_2P)

            shooting_percent_0_3 = shooting_cols[10].xpath('text()').extract_first()
            player_data['shooting_percent_0_3'] = get_float_val(shooting_percent_0_3)
            
            shooting_percent_3_10 = shooting_cols[11].xpath('text()').extract_first()
            player_data['shooting_percent_3_10'] = get_float_val(shooting_percent_3_10)

            shooting_percent_10_16 = shooting_cols[12].xpath('text()').extract_first()
            player_data['shooting_percent_10_16'] = get_float_val(shooting_percent_10_16)
            
            shooting_percent_16_l3 = shooting_cols[13].xpath('text()').extract_first()
            player_data['shooting_percent_16_l3'] = get_float_val(shooting_percent_16_l3)

            shooting_percent_3P = shooting_cols[14].xpath('text()').extract_first()
            player_data['shooting_percent_3P'] = get_float_val(shooting_percent_3P)

            shooting_FG_percent_0_3 = shooting_cols[16].xpath('text()').extract_first()
            player_data['shooting_FG_percent_0_3'] = get_float_val(shooting_FG_percent_0_3)

            shooting_FG_percent_3_10 = shooting_cols[17].xpath('text()').extract_first()
            player_data['shooting_FG_percent_3_10'] = get_float_val(shooting_FG_percent_3_10)

            shooting_FG_percent_10_16 = shooting_cols[18].xpath('text()').extract_first()
            player_data['shooting_FG_percent_10_16'] = get_float_val(shooting_FG_percent_10_16)

            shooting_FG_percent_16_l3 = shooting_cols[19].xpath('text()').extract_first()
            player_data['shooting_FG_percent_16_l3'] = get_float_val(shooting_FG_percent_16_l3)

            shooting_FG_percent_ast_2P = shooting_cols[21].xpath('text()').extract_first()
            player_data['shooting_percent_ast_2P'] = get_float_val(shooting_FG_percent_ast_2P)
            
            shooting_percent_FG_dunks = shooting_cols[22].xpath('text()').extract_first()
            player_data['shooting_percent_FG_dunks'] = get_float_val(shooting_percent_FG_dunks)

            shooting_made_dunks = shooting_cols[23].xpath('text()').extract_first()
            player_data['shooting_made_dunks'] = get_int_val(shooting_made_dunks)

            shooting_percent_ast_3P = shooting_cols[24].xpath('text()').extract_first()
            player_data['shooting_percent_ast_3P'] = get_float_val(shooting_percent_ast_3P)

            shooting_percent_3P_corner = shooting_cols[25].xpath('text()').extract_first()
            player_data['shooting_percent_3P_corner'] = get_float_val(shooting_percent_3P_corner)

            shooting_FG_percent_3P_corner = shooting_cols[26].xpath('text()').extract_first()
            player_data['shooting_FG_percent_3P_corner'] = get_float_val(shooting_FG_percent_3P_corner)
            
        else:
          for player_data in player_data_objs:
            initialize_shooting_none(player_data)
        

        pbp_rows = sel.xpath('//table[@id="advanced_pbp"]//tr[@class="full_table"]')
        if pbp_rows:
          offset = 0
          if len(pbp_rows) != len(per_game_rows):
            offset = len(per_game_rows) - len(shooting_rows)
          if offset != 0:
            for i in range(offset):
              initialize_pbp_none(player_data_objs[i])
              yield player_data_objs[i]
          for k,row in enumerate(pbp_rows):
            pbp_cols = row.xpath('td')
            player_data = player_data_objs[k+offset]
            
            pbp_PG_percent = pbp_cols[7].xpath('text()').extract_first()
            player_data['pbp_PG_percent'] = remove_percent_get_float(pbp_PG_percent)
  
            pbp_SG_percent = pbp_cols[8].xpath('text()').extract_first()
            player_data['pbp_SG_percent'] = remove_percent_get_float(pbp_SG_percent)

            pbp_SF_percent = pbp_cols[9].xpath('text()').extract_first()
            player_data['pbp_SF_percent'] = remove_percent_get_float(pbp_SF_percent)

            pbp_PF_percent = pbp_cols[10].xpath('text()').extract_first()
            player_data['pbp_PF_percent'] = remove_percent_get_float(pbp_PF_percent)
           
            pbp_C_percent = pbp_cols[11].xpath('text()').extract_first()
            player_data['pbp_C_percent'] = remove_percent_get_float(pbp_C_percent)

            pbp_plusminus_oncourt = pbp_cols[12].xpath('text()').extract_first()
            player_data['pbp_plusminus_oncourt'] = get_float_val(pbp_plusminus_oncourt)

            pbp_plusminus_onoff = pbp_cols[13].xpath('text()').extract_first()
            player_data['pbp_plusminus_onoff'] = get_float_val(pbp_plusminus_onoff)
            
            pbp_TOV_badpass = pbp_cols[14].xpath('text()').extract_first()
            player_data['pbp_TOV_badpass'] = get_int_val(pbp_TOV_badpass)

            pbp_TOV_lostball = pbp_cols[15].xpath('text()').extract_first()
            player_data['pbp_TOV_lostball'] = get_int_val(pbp_TOV_lostball)

            pbp_TOV_other = pbp_cols[16].xpath('text()').extract_first()
            player_data['pbp_TOV_other'] = get_int_val(pbp_TOV_other)

            pbp_shooting_foul_comm = pbp_cols[17].xpath('text()').extract_first()
            player_data['pbp_shooting_foul_comm'] = get_int_val(pbp_shooting_foul_comm)
            
            pbp_blocking_foul_comm = pbp_cols[18].xpath('text()').extract_first()
            player_data['pbp_blocking_foul_comm'] = get_int_val(pbp_blocking_foul_comm)

            pbp_offensive_foul_comm = pbp_cols[19].xpath('text()').extract_first()
            player_data['pbp_offensive_foul_comm'] = get_int_val(pbp_offensive_foul_comm)
            
            pbp_take_foul_comm = pbp_cols[20].xpath('text()').extract_first()
            player_data['pbp_take_foul_comm'] = get_int_val(pbp_take_foul_comm)
            
            pbp_PGA = pbp_cols[21].xpath('text()').extract_first()
            player_data['pbp_PGA'] = get_int_val(pbp_PGA)
            
            pbp_Sfdrawn = pbp_cols[22].xpath('text()').extract_first()
            player_data['pbp_Sfdrawn'] = get_int_val(pbp_Sfdrawn)

            pbp_And1 = pbp_cols[23].xpath('text()').extract_first()
            player_data['pbp_And1'] = get_int_val(pbp_And1)
            
            pbp_FGA_blocked = pbp_cols[24].xpath('text()').extract_first()
            player_data['pbp_FGA_blocked'] = get_int_val(pbp_FGA_blocked)
            
            yield player_data
        else:
          for player_data in player_data_objs:
            initialize_pbp_none(player_data)
            yield player_data

