import pandas
import requests
import json
from ast import literal_eval
import mysql.connector

html_url = 'https://www.basketball-reference.com/leagues/NBA_2019_standings.html'
r = requests.get(html_url)
beef = r.text
pd = pandas.read_html(beef)	

def NBATeams(df):
    split = df['team'].str.split(" ", n=2, expand=True)
    scraps = split[2].to_list()
    names = split[1].to_list()
    for i in range(0, len(names)):
        if names[i] == 'ers':
            names[i] = '76ers'
        if scraps[i] != None:
            if names[i] != 'Trail':
                names[i] = scraps[i]
            else:
                names[i] = names[i] + ' ' + scraps[i]
    
    df['team'] = names
    
def pandaToJson(data, txt, json):
    with open(txt, "w") as f:
        f.write(str(data))

    fin = open(txt, "rt")
    fout = open(json, "wt")

    for line in fin:
        fout.write(line.replace("'", '"'))
    
    fin.close()
    fout.close()


def checkFloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False       
dfe = pd[0]
dfe = dfe.rename(columns={'Eastern Conference': 'team', 'W/L%': 'PCT'})
dfe = dfe[['team', 'W', 'L', 'PCT', 'GB']]
dfe['conf'] = 'East'
dfe['team'] = dfe['team'].str.replace('*','', regex=True)
NBATeams(dfe)
dfw = pd[1]
dfw = dfw.rename(columns={'Western Conference': 'team', 'W/L%': 'PCT'})
dfw = dfw[['team', 'W', 'L', 'PCT', 'GB']]
dfw['conf'] = 'West'
dfw['team'] = dfw['team'].str.replace('*','', regex=True)
NBATeams(dfw)
nba = dfe.append(dfw, ignore_index = True)
nba['W'] = nba['W'].astype(int)
nba['L'] = nba['L'].astype(int)
nba = nba.sort_values(by='team')
gbchk = nba['GB'].to_list()

for i in range(0,30):
    if checkFloat(gbchk[i]):
        float(gbchk[i])
    else:
        gbchk[i] = float(0)

nba['GB'] = gbchk
nba['GB'] = nba['GB'].astype(float)

standings_json_file = 'C:/xampp/htdocs/MitchellSync/website/almanac/NBA/standings.json'
standings_text_file = 'C:/xampp/htdocs/MitchellSync/website/almanac/NBA/standings.txt'

jsdf = nba.to_json(orient='records')
js_std = json.loads(jsdf)
pandaToJson(js_std, standings_text_file, standings_json_file)