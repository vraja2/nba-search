from flask import render_template
from nbasearch import app, player_dict, team_dict, player_list
import json

@app.route('/')
def index():
  return render_template("index.html", player_list=json.dumps(player_list))
  #return str(team_dict[player_dict['Michael Jordan'][0][-1]])

def get_teammates():
  rebound_range = 2
  points_range = 4

