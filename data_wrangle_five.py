import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def make_even(num):
    odd = num %2
    return num+odd

def write_xls(df, name):
    writer = pd.ExcelWriter(name)
    df.to_excel(writer)
    writer.save()

def odds_id_matcher(id_list, onl, ongl):
    odds_id_game_list = []
    for i in range(0, len(ongl)):
        name = ongl[i]
        for j in range(0, len(onl)):
            if onl[j] == name:
                odds_id_game_list.append(id_list[j])
                break
            elif j == (len(onl)-1):
                odds_id_game_list.append('No match')
    return odds_id_game_list

def low_parity_moneyline_maker(ml,close):
    ml = ml.to_list()
    close = close.to_list()
    close_floats = []
    close = [0 if x == 'pk' or x =='NL' else x for x in close]
    for item in close:
        close_floats.append(float(item))
    new_ml = []
    for x in range(0,len(ml)):
        if ml[x] == 'NL':
            if close_floats[x] < 80 and close_floats[x]> 20:
                new_ml.append(-8000)
            else:
                new_ml.append('Underdog?')
        else:
            new_ml.append(int(ml[x]))
    print(close_floats)
    return new_ml

#Import starting data
o_2011 = pd.read_excel(r'/Users/stevenkerr/PycharmProjects/ncaa_shot_clock/odds_data/NCAA Odds 11-12.xlsx')
ss_2011 = pd.read_excel('NCAA Schools 11-12.xlsx', header=1)

#Give same game ID to both teams playing in a game for the odds data
o_2011['Game ID'] = [x for x in range(1,1+len(o_2011['Rot']))]
o_2011['t_num'] = np.where(o_2011['Rot'] % 2, 0, 1)
o_2011['Game ID'] = o_2011['Game ID'].apply(make_even)

#Read in id_master, add team ID number for each team in odds data
id_master = pd.read_excel('id_master.xlsx')
id_list = id_master['ID'].to_list()
odds_name_list = id_master['Odds name'].to_list()
odds_name_game_list = o_2011['Team'].to_list()
o_2011['team_id'] = odds_id_matcher(id_list,odds_name_list,odds_name_game_list)

#Remove odds data observations of teams that are not in the season stats data
o_2011 = o_2011[o_2011['team_id'] != 'No match']

#add on season stats to each team observation in odds data using team ids (Rk for season stats data)
o_2011 = o_2011.merge(ss_2011, left_on= 'team_id', right_on= 'Rk')

#resort data by game id (to put games in chronilogical order)
o_2011 = o_2011.sort_values(by=['Game ID'])

#Remove redundant and other unuseful features
o_2011 = o_2011.drop(['W.1','L.1','W.2','L.2','W.3','L.3','2H','Open','Rk','School','Unnamed: 16'],axis=1)

#Make multi-level index and unstack to make each game an observation
o_2011 =o_2011.set_index(['Game ID', 't_num'])
o_2011 =o_2011.unstack(level = -1)

#Write new data into a spreadsheet
write_xls(o_2011,'2011newclean.xlsx')
print(o_2011.info())

#write_xls(merged, '2011cleanmerged.xlsx')

