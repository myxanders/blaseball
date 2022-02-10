import pandas
import requests
import mysql.connector
import json

html_url = 'https://www.espn.com/nhl/standings/_/season/2018'
r = requests.get(html_url)
beef = r.text
standings_json_file = 'C:/xampp/htdocs/MitchellSync/website/almanac/NHL/standings.json'
standings_text_file = 'C:/xampp/htdocs/MitchellSync/website/almanac/NHL/standings.txt'
def pandaToJson(data, txt, json):
    with open(txt, "w") as f:
        f.write(str(data))

    fin = open(txt, "rt")
    fout = open(json, "wt")

    for line in fin:
        fout.write(line.replace("'", '"'))
    
    fin.close()
    fout.close()
pd = pandas.read_html(beef)
df = pd[0]
df = df[0].str.slice(4,7)
df = df.replace({'TBT': 'TB', 'NJN': 'NJ'})
df = df.drop([0,9])
tshos = df.to_list()
dfe = pd[1]
dfe = dfe.drop([0,9])
dfe.insert(0,'tsho',tshos)
dfe = dfe.rename(columns={1:'W', 2:'L', 3: 'OTL', 4: 'PTS', 5: 'ROW', 10: 'GF', 11: 'GA'})
dfe = dfe[['tsho', 'W', 'L', 'OTL', 'PTS', 'ROW', 'GF', 'GA']]

dfb = pd[2]
dfb = dfb[0].str.slice(4,7)
dfb = dfb.drop([0,8])
dfb = dfb.replace({'ARI': 'ARZ', 'SJS':'SJ', 'LAL':'LA'})
wtshos = dfb.to_list()
dfw = pd[3]
dfw = dfw.drop([0,8])
dfw.insert(0,'tsho',wtshos)
dfw = dfw.rename(columns={1:'W', 2:'L', 3: 'OTL', 4: 'PTS', 5: 'ROW', 10: 'GF', 11: 'GA'})
dfw = dfw[['tsho', 'W', 'L', 'OTL', 'PTS', 'ROW', 'GF', 'GA']]
nhl = dfe.append(dfw, ignore_index = True)
nhl[['W', 'L','OTL', 'PTS', 'ROW', 'GF', 'GA']] = nhl[['W', 'L','OTL', 'PTS', 'ROW', 'GF', 'GA']].astype(int)
nhl = nhl.sort_values(by='tsho')
mydb = mysql.connector.connect(
    host="localhost",
    user="myxanders",
    passwd="a8TJuJ6WrpQ8WY",
    database="mitchellsync"
)	
mycursor = mydb.cursor(dictionary=True)
mycursor.execute('SELECT teamShort, team, division FROM nhlteams ORDER BY teamShort ASC')
result = mycursor.fetchall()
fullnames = []
division = []
for r in result:
    name = r['team']
    if name == 'Kraken':
        continue
    div = r['division']
    fullnames.append(name)
    division.append(div)
nhl.insert(1, 'team', fullnames)
nhl['div'] = division
jsdf = nhl.to_json(orient='records')
js_std = json.loads(jsdf)
pandaToJson(js_std, standings_text_file, standings_json_file)
