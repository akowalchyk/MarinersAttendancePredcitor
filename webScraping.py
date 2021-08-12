
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from threading import Timer

team = 'SEA'

def get_games():
    df = pd.DataFrame(columns=['date', 'box', 'team', 'at', 'opponent', 'w_or_l', 'runs', 'runs_allowed',
                                           'innings', 'record', 'div_rank', 'gb', 'winning_pitcher', 'losing_pitcher',
                                           'save', 'time', 'd_or_n', 'attendance','cLI', 'streak', 'Orig. Scheduled', 'winning_percentage'])
    years = []
    total_games_played = []
    for year in range (1994,2022):
            print(year)
            try:
                temp_df = pd.DataFrame(columns=['date', 'box', 'team', 'at', 'opponent', 'w_or_l', 'runs', 'runs_allowed',
                                           'innings', 'record', 'div_rank', 'gb', 'winning_pitcher', 'losing_pitcher',
                                           'save', 'time', 'd_or_n', 'attendance','cLI', 'streak', 'Orig. Scheduled'])
                html = requests.get('http://www.baseball-reference.com/teams/' + team + '/' + str(year) +
                                    '-schedule-scores.shtml')
                bs = BeautifulSoup(html.text, 'html.parser')
                game_count = 0
                for game in bs.find('table', {'class':'stats_table'}).find_all('tr'):
                    results = []
                    for element in game.find_all('td'):
                        results.append(element.text)
                        if(len(results) == 21):
                            temp_df.loc[len(temp_df)] = results
                            years.append(year)
                            total_games_played.append(game_count)
                            game_count += 1

                

                df = pd.concat([df, temp_df]).reset_index(drop=True)

            except:
                print("damn")
                pass
    
    # adding years collumn
    df['year'] = years

    # adding total games collumn
    df['total_games_played'] = total_games_played

    #replacing empty strings with NaN values
    df.attendance.replace("", None, inplace=True)

     # dropping all away games
    df = df[~df['at'].str.contains('@')].reset_index(drop=True)

    df.drop(df.loc[df['year']==2020].index, inplace=True)

    df = df[df.attendance.notna()]

    df.attendance = df.attendance.str.replace(',', '').astype(int)

    # adding win percentage column
    win_pct_col = []
    for x in df.record:
        win_loss = x.split('-')
        wins = int(win_loss[0])
        losses = int(win_loss[1])
        total = wins + losses
        win_pct_col.append(round(wins / total, 3))

    df['winning_percentage'] = win_pct_col 
    #adding weeekday/weekend col
    day_of_week_col = []
    month_col = []
    weekday = ['Monday', 'Tuesday',  'Wednesday', 'Thursday']
    weekend = ['Friday', 'Saturday', 'Sunday']
    for x in df.date:
        date_split = x.split(',')
        day_of_week = date_split[0]
        year_day_split = date_split[1].split(' ')
        month = year_day_split[1]
        month_col.append(month)
        if day_of_week in weekday:
            day_of_week_col.append(1)
        else:
            day_of_week_col.append(0)
    df['weekday'] = day_of_week_col
    df['month'] = month_col

    # creating night game column
    night_col =[]
    for x in df.d_or_n:
        if x == 'D':
            night_col.append(0)
        else:
            night_col.append(1)
    df['night_game'] = night_col

    #converting gb to floats
    df.gb = [0. if x == ' Tied' or x == '0'
         else float(x.replace('up', '')) if 'up' in x
         else -float(x)
         for x in df.gb]

    # adding Top 5 opponent column
    pop_opp = []
    for x in df.opponent:
        if x == "BOS" or x == "NYY" or x == "LAD" or x == "ANA" or x == "SFG":
            pop_opp.append(1)
        else:
            pop_opp.append(0)
    df["pop_opp"] = pop_opp
    



    # dropping uninportant columns
    df = df.drop(['team','box','at', 'w_or_l', 'runs', 'runs_allowed', 'innings', 'record', 'winning_pitcher','losing_pitcher', 
    'save','time', 'd_or_n', 'streak', 'Orig. Scheduled'], axis=1)



    df.to_csv('data.csv', index=False)
    return df

    
x=datetime.today()
y=x.replace(day=x.day+1, hour=1, minute=0, second=0, microsecond=0)
delta_t=y-x

secs=delta_t.seconds+1

t = Timer(secs, get_games())
t.start()