import requests

url = 'http://localhost:5000/results'
r = requests.post(url,json={'year':2005, 'weekday': 0, 'winning_percentage':0.561, 'total_games_played': 20, 'pop_opp': 1})

print(r.json())