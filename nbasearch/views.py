from nbasearch import app, player_dict, team_dict

@app.route('/')
def index():
  #simple test to see if dictionaries produce expected results
  return str(team_dict[player_dict['Michael Jordan'][0][0]])
