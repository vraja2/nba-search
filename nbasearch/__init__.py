import json
import pickle
import os
from collections import defaultdict
from flask import Flask
app = Flask(__name__)

@app.before_first_request
def init_data():
  init_player_data()
  init_team_data()
  init_player_list()

def open_file(file_path):
  return open(os.path.join(os.path.dirname(__file__),file_path))

#map from player name to list of lists (multiple players with same name) of teams played for
player_dict = defaultdict(list)

def init_player_data():
  f = open_file('static/pickle/playerdata.pickle')
  while True:
    try:
      player = pickle.load(f)
    except EOFError:
      break
    else:
      player_name = player['player_name'] 
      teams_played_on = player['teams_played_on']
      if teams_played_on:
        first_year = teams_played_on[0][1]
        last_year = teams_played_on[-1][1]
        player_dict[(player_name,first_year,last_year)].append(player['teams_played_on'])

#map from (team_name,year) to point/rebound ranges. rebound range is index 0, points range is 1
team_dict = defaultdict(list)

def init_team_data():
  f = open_file('static/pickle/teamdata.pickle')
  while True:
    try:
      team = pickle.load(f)
    except EOFError:
      break
    else:
      key_tup = (team['team'],team['year'])
      team_dict[key_tup].append(team['rebound_ranges'])
      team_dict[key_tup].append(team['points_ranges'])

player_list = []

def init_player_list():
  for player_tuple,player_teams in player_dict.iteritems():
      player_list.append('{} ({}-{})'.format(player_tuple[0],player_tuple[1],player_tuple[2]))

import nbasearch.views
