import pandas
import requests
# from config import mydb, year, szn_scheds, pandaToJson
import json
import mysql.connector

def pandaToJson(data, txt, json):
    with open(txt, "w") as f:
        f.write(str(data))

    fin = open(txt, "rt")
    fout = open(json, "wt")

    for line in fin:
        fout.write(line.replace("'", '"'))
    
    fin.close()
    fout.close()
html_url = 'https://www.espn.com/mlb/standings/_/season/2021'
r = requests.get(html_url)
beef = r.text
standings_json_file = 'C:/xampp/htdocs/MitchellSync/website/almanac/MLB/standings.json'
standings_text_file = 'C:/xampp/htdocs/MitchellSync/website/almanac/MLB/standings.txt'
pd = pandas.read_html(beef)
df = pd[0]
df = df[0].str.slice(4,7)
df = df.drop([0,6,12])
df = df.replace({'TBT':'TB', 'KCK':'KC', 'CHW':'CWS'})
tshos = df.to_list()
df_b = pd[1]
df_b = df_b.drop([0,6,12])
df_b.insert(0,'tsho', tshos)
df_b = df_b.rename(columns={0:'W', 1:'L', 2:'PCT'})
df_b = df_b[['tsho', 'W', 'L', 'PCT']]

df_nl = pd[2]
df_nl = df_nl[0].str.slice(4,7)
df_nl = df_nl.drop([0,6,12])
df_nl = df_nl.replace({'SFS':'SF', 'SDS':'SD', 'ARI':'ARZ', 'WSH':'WAS'})
nl_tshos = df_nl.to_list()
df_nl_b = pd[3]
df_nl_b = df_nl_b.drop([0,6,12])
df_nl_b.insert(0, 'tsho', nl_tshos)
df_nl_b = df_nl_b.rename(columns={0:'W', 1:'L', 2:'PCT'})
df_nl_b = df_nl_b[['tsho', 'W', 'L', 'PCT']]
df_b = df_b.append(df_nl_b, ignore_index = True)
df_b['W'] = df_b['W'].astype(int)
df_b['L'] = df_b['L'].astype(int)
df_b = df_b.sort_values(by='tsho')
mydb = mysql.connector.connect(
    host="localhost",
    user="myxanders",
    passwd="a8TJuJ6WrpQ8WY",
    database="mitchellsync"
)
mycursor = mydb.cursor(dictionary=True)
mycursor.execute('SELECT teamShort, team FROM mlbteams WHERE teamShort != "TBD" ORDER BY teamShort ASC')
result = mycursor.fetchall()
fullnames = []
for r in result:
    name = r['team']
    fullnames.append(name)

df_b.insert(1, 'team', fullnames)
jsdf = df_b.to_json(orient='records')
js_std = json.loads(jsdf)
pandaToJson(js_std, standings_text_file, standings_json_file)
