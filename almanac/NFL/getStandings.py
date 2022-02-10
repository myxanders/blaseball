import pandas
import json
from ast import literal_eval
import mysql.connector

mydb = mysql.connector.connect(
    host="mitchellsync.sytes.net",
    user="myxanders",
    passwd="a8TJuJ6WrpQ8WY",
    database="mitchellsync"
)	

nfl_info = pandas.read_sql('SELECT team, teamShort, conference, division FROM nflteams ORDER BY teamShort ASC', con=mydb)

def pandaToJson(data, txt, json):
    with open(txt, "w") as f:
        f.write(str(data))

    fin = open(txt, "rt")
    fout = open(json, "wt")

    for line in fin:
        fout.write(line.replace("'", '"'))
    
    fin.close()
    fout.close()

json_file = 'C:/xampp/htdocs/MitchellSync/website/almanac/NFL/teamSched.json'
standings_json_file = 'C:/xampp/htdocs/MitchellSync/website/almanac/NFL/standings.json'
standings_text_file = 'C:/xampp/htdocs/MitchellSync/website/almanac/NFL/standings.txt'
playoffs_text = 'C:/xampp/htdocs/MitchellSync/website/almanac/NFL/playoffs.txt'
f = open(json_file)
data = json.load(f)
sos_nfl = []
sov_nfl = []
victories = []
standings = pandas.DataFrame(columns = ["Team", "W", "L", "T", "PCT", "PF", "PA", "PD", "Div", "Div Pct", "Conf", "Conf Pct", "conference", "division"])

def compileStandings(nfl_team):
    w = 0
    l = 0
    t = 0
    c_w = 0
    c_l = 0
    c_t = 0
    d_w = 0
    d_l = 0
    d_t = 0
    pf = 0
    pa = 0
    for n in data[nfl_team]:
        tm = nfl_info.loc[nfl_info['team'] == nfl_team]
        div = tm.iloc[0]['division']
        conf = tm.iloc[0]['conference']
        team = tm.iloc[0]['team']
        opp = n['Opponent']
        if opp == 'BYE':
            continue
        r = nfl_info.loc[nfl_info['team'] == opp]
        opp_c = r.iloc[0]['conference']
        opp_d = r.iloc[0]['division']
        if opp_c == conf:
            if n['Result'] == 'W':
                c_w +=1
            elif n['Result'] == 'L':
                c_l +=1
            elif n['Result'] == 'T':
                c_t +=1
            
            if opp_d == div:
                if n['Result'] == 'W':
                    d_w +=1
                elif n['Result'] == 'L':
                    d_l +=1
                elif n['Result'] == 'T':
                    d_t +=1
                
        if n['Result'] == 'W':
            w += 1
        elif n['Result'] == 'L':
            l += 1  
        elif n['Result'] == 'T':
            t += 1

        score_trim = n['Score'].split("-")
        if score_trim[0] != '':
            pts = int(score_trim[0])
            pta = int(score_trim[1])
            pf = pf + pts
            pa = pa + pta

    gp = w+l+t
    c_gp = c_w+c_l+c_t
    d_gp = d_w+d_l+d_t

    if gp > 0:
        pct = round((w+(.5*t)) / gp, 3)
    if c_gp > 0:
        c_pct = round((c_w+(.5*c_t)) / c_gp, 3)
    if d_gp > 0:
        d_pct = round((d_w+(.5*c_t)) / d_gp, 3)

    pd = pf - pa
    div_wl = str(d_w) + '-' + str(d_l)
    if d_t > 0:
        div_wl = div_wl + '-' + str(d_t)
    conf_wl = str(c_w) + '-' + str(c_l)
    if c_t > 0:
        conf_wl = conf_wl + '-' + str(c_t)
    team = {"Team": team, "W": w, "L": l, "T": t, "PCT": pct, "PF": pf, "PA": pa, "PD": pd, "Div": div_wl, "Div Pct": d_pct, "Conf": conf_wl, "Conf Pct": c_pct, "conference": conf, "division": div}
    return team

def strengthSolver(team):
    json_file = 'C:/xampp/htdocs/MitchellSync/website/almanac/NFL/teamSched.json'
    f= open(json_file)
    json_data = json.load(f)
    tm_sched = json_data[team]
    sos_top = 0
    sos_bot = 0
    sov_top = 0
    sov_bot = 0
    beat = []
    for wk in tm_sched:
        opp = wk['Opponent']
        if opp != 'BYE':
            row = standings[standings['Team'] == opp]
            w = row.iloc[0]["W"]
            l = row.iloc[0]["L"]
            t = row.iloc[0]["T"]
            gp = w + l + t
            if wk['Score'] != '~~~' and wk['Score'] != '~~~':
                if wk['Result'] == 'W':
                    sov_top = sov_top + int(w)
                    sov_bot = sov_bot + int(gp)
                    beat.append(opp)

                sos_top = sos_top + int(w)
                sos_bot = sos_bot + int(gp)
            
    if sos_bot == 0:
        sos_bot = 1
    if sov_bot == 0:
        sov_bot = 1
    sos = round(sos_top / sos_bot, 3)
    sov = round(sov_top / sov_bot, 3)
    sos_nfl.append(sos)
    sov_nfl.append(sov) 
    #Need to make the list a string in order to evaluate it as a list rather than a single object for tiebreaking purproses
    victories.append(str(beat))
    f.close()    

for x in data:
    entry = compileStandings(x)
    standings = standings.append(entry, ignore_index=True)

for x in data:
    strengthSolver(x)

standings['SOS'] = sos_nfl
standings['SOV'] = sov_nfl
standings['Beat'] = victories
standings['divh2h'] = 0
standings['confh2h'] = 0

def confStandings(conf):
    divisionTies(conf, standings)
    breakCTies(conf, standings)
    conference = standings.loc[standings['conference'] == conf].sort_values(['PCT', 'confh2h', 'divh2h', 'Conf Pct', 'SOV', 'SOS'], ascending = (False, False, False, False, False, False))
    leaders = conference.groupby('division').first().sort_values(['PCT', 'confh2h', 'Conf Pct', 'SOV', 'SOS'], ascending = (False, False, False, False, False))
    for i in range(0,4):
        tsho = leaders.iloc[i]['Team']
        conference = conference[conference['Team'] != tsho]

    wild_card = conference.sort_values(['PCT', 'confh2h', 'Conf Pct', 'SOV', 'SOS'], ascending = (False, False, False, False, False))
    leaders = leaders.append([wild_card.iloc[0], wild_card.iloc[1], wild_card.iloc[2]])


#One of the early tiebreakers is head-to-head. So we check who has defeated teams they're tied with
def breakCTies(conf, nfl):
    fc = nfl.loc[nfl['conference'] == conf].sort_values(by='PCT')
    fc_ties = fc[fc.duplicated('PCT', keep=False)].groupby('PCT')['Team'].apply(list).reset_index()
    i = 0
    while i < fc_ties.shape[0]:
        tied = fc_ties.iloc[i]['Team']
        for tm in tied:
            trow = nfl.loc[nfl['Team'] == tm]
            beat = literal_eval(trow['Beat'].values[0])
            tiebreak = list(set.intersection(set(tied), set(beat)))
            ch2h = len(tiebreak)
            x = trow.index.values[0]
            nfl.at[x, 'confh2h'] = ch2h
        i += 1

def divisionTies(conf, nfl):
    fc = nfl.loc[nfl['conference'] == conf].sort_values(by='PCT')
    north = fc.loc[fc['division'] == 'North'].sort_values(by='PCT')
    breakDTies(north, standings)
    south = fc.loc[fc['division'] == 'South'].sort_values(by='PCT')
    breakDTies(south, standings)
    east = fc.loc[fc['division'] == 'East'].sort_values(by='PCT')
    breakDTies(east, standings)
    west = fc.loc[fc['division'] == 'West'].sort_values(by='PCT')
    breakDTies(west, standings)
    

def breakDTies(div, nfl):
    ties = div[div.duplicated('PCT', keep=False)].groupby('PCT')['Team'].apply(list).reset_index()
    if ties.shape[0] > 0:
        i = 0
        while i < ties.shape[0]:
            tied = ties.iloc[i]['Team']
            for tm in tied:
                trow = nfl.loc[nfl['Team'] == tm]
                beat = literal_eval(trow['Beat'].values[0])
                tiebreak = list(set.intersection(set(tied), set(beat)))
                dh2h = len(tiebreak)
                x = trow.index.values[0]
                nfl.at[x, 'divh2h'] = dh2h
            i += 1

confStandings('NFC')
confStandings('AFC')
# #Not necessary to drop the column but the column is no longer necessary either
standings = standings.drop(columns='Beat')
jsdf = standings.to_json(orient='records')
js_std = json.loads(jsdf)
pandaToJson(js_std, standings_text_file, standings_json_file)