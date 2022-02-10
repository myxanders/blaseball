import requests
import json
import pandas

r = requests.get("https://www.pro-football-reference.com/years/2009/games.htm")
meat = r.text
pd = pandas.read_html(meat)
df = pd[0]
df = df.rename(columns={'Unnamed: 5': 'location'})
df = df.reset_index()

hometeams = []
homescores = []
awayteams = []
awayscores = []
weeks = []
for index, row in df.iterrows():
    if row['Week'] == 'Week' or row['Date'] == 'Playoffs':
        continue
    if row['location'] == '@' or row['location'] == 'N':
        home = row['Loser/tie']
        homepts = row['PtsL']
        away = row['Winner/tie']
        awaypts = row['PtsW']
    else:
        away = row['Loser/tie']
        awaypts = row['PtsL']
        home = row['Winner/tie']
        homepts = row['PtsW']

    hometeams.append(home)
    awayteams.append(away)
    homescores.append(homepts)
    awayscores.append(awaypts)
    weeks.append(row['Week'])

data = {}
nfl = pandas.DataFrame()
nfl['week'] = weeks
nfl['homescore'] = homescores
nfl['hometeam'] = hometeams
nfl['awayteam'] = awayteams
nfl['awayscore'] = awayscores

nfl['hometeam'] = nfl['hometeam'].str.split().str[-1]
nfl['awayteam'] = nfl['awayteam'].str.split().str[-1]
nfl = nfl.replace({'WildCard': 18, 'Division': 19, 'ConfChamp': 20, 'SuperBowl': 21})
nfl = nfl.replace({'Redskins':'Washington', '49ers': 'Niners'})
nfl['week'] = nfl['week'].astype(int)

# for i in range (1,22):
#     wknum = 'week' + str(i)
#     slate = nfl[nfl.week == i]
#     nfl_js = slate.to_json(orient='records')
#     data[wknum] = json.loads(nfl_js)

nfl_js = nfl.to_json(orient='records')
data = json.loads(nfl_js)

weekly_json = 'C:/xampp/htdocs/MitchellSync/website/almanac/NFL/weeklySched.json'
weekly_txt = 'C:/xampp/htdocs/MitchellSync/website/almanac/NFL/weeklySched.txt'

def pandaToJson(data, txt, json):
    with open(txt, "w") as f:
        f.write(str(data))

    fin = open(txt, "rt")
    fout = open(json, "wt")

    for line in fin:
        fout.write(line.replace("'", '"'))
    
    fin.close()
    fout.close()

pandaToJson(data, weekly_txt, weekly_json)