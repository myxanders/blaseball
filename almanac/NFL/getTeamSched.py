import json
import pandas

def pandaToJson(data, txt, json):
    with open(txt, "w") as f:
        f.write(str(data))

    fin = open(txt, "rt")
    fout = open(json, "wt")

    for line in fin:
        fout.write(line.replace("'", '"'))
    
    fin.close()
    fout.close()

def checkInt(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def determineBye(weeks):
    for i in range(1,18):
        if i not in weeks:
            return i

teams = ['Cardinals', 'Falcons', 'Ravens', 'Bills', 'Panthers', 'Bears', 'Bengals', 'Browns', 'Cowboys', 'Broncos', 'Lions', 'Packers', 'Texans', 'Colts', 'Jaguars', 'Chiefs', 'Chargers', 'Rams', 'Raiders', 'Dolphins', 'Vikings', 'Patriots', 'Saints', 'Giants', 'Jets', 'Eagles', 'Steelers', 'Seahawks', 'Niners', 'Buccaneers', 'Titans', 'Commanders']
nfl_data = {}
team_txt_sched = 'C:/xampp/htdocs/MitchellSync/website/almanac/NFL/teamSched.txt'
team_json_sched = 'C:/xampp/htdocs/MitchellSync/website/almanac/NFL/teamSched.json'

def teamJsonSchedule(team):
    json_file = 'C:/xampp/htdocs/MitchellSync/website/almanac/NFL/weeklySched.json'
    f = open(json_file)
    data = json.load(f)
    data = pandas.DataFrame(data)
    team_schedule = []
    df = data[(data['hometeam'] == team) | (data['awayteam'] == team)]
    played = df['week'].to_list()
    bye = determineBye(played)
    i = 1
    while i <= 17:
        if i == bye:
            opp = 'BYE'
            pf = '~~~'
            pa = '~~~'
            outcome = 'B'
        else:
            row = df.loc[df['week'] == i]
            home = row.iloc[0]['hometeam']
            away = row.iloc[0]['awayteam']
            hscore = row.iloc[0]['homescore']
            ascore = row.iloc[0]['awayscore']
            if home == team:
                pf = int(hscore)
                pa = int(ascore)
                opp = away
            elif away == team:
                pf = int(ascore)
                pa = int(hscore)
                opp = home 
            
            if pf > pa:
                outcome = 'W'
            elif pf < pa:
                outcome = 'L'
            elif pf == pa:
                outcome = 'T'

            score = str(pf) + '-' + str(pa) 

        game_data = {'Week': i, 'Opponent': opp, 'Score': score, 'Result': outcome}
        team_schedule.append(game_data)       
        i += 1
    nfl_data[team] = team_schedule

    # for tm in teams:
    #     df = data[data['hometeam'] == tm or data['awayteam'] == tm]

    # for i in data:
    #     games = len(data[i])
    #     #Don't put playoff games into the team schedule
    #     if games <= 6:
    #         continue
    #     score = None
    #     opp = None
    #     oppscore = None
    #     outcome = None
    #     count = 0
    #     for n in range(0,games):
    #         if data[i][n]['Home Team'] == team:
    #             score = data[i][n]['Home Score']
    #             opp = data[i][n]['Away Team']
    #             oppscore = data[i][n]['Away Score']
    #             check = checkInt(score)
    #             if check == False:
    #                 outcome = ''
    #                 break
    #             score = int(score)
    #             oppscore = int(oppscore)
    #             if score > oppscore:
    #                 outcome = 'W'
    #             elif score < oppscore:
    #                 outcome = 'L'
    #             elif score != '' and score == oppscore:
    #                 outcome = 'T'
    #             break
    #         elif data[i][n]['Away Team'] == team:
    #             score = data[i][n]['Away Score']
    #             opp = '@' + data[i][n]['Home Team']
    #             oppscore = data[i][n]['Home Score']
    #             check = checkInt(score)
    #             if check == False:
    #                 outcome = ''
    #                 break           
    #             score = int(score)
    #             oppscore = int(oppscore)                     
    #             if score > oppscore:
    #                 outcome = 'W'
    #             elif score < oppscore:
    #                 outcome = 'L'
    #             elif score != '' and score == oppscore:
    #                 outcome = 'T'                
    #             break
    #         else:
    #             count += 1
            
    #         if count == games:
    #             opp = 'BYE'
    #             outcome = '~~~'

    #     if opp != 'BYE':
    #         final_score = str(score) + '-' + str(oppscore)
    #     else:
    #         final_score = '~~~'
    #     game_data = {'Opponent': opp, 'Score': final_score, 'Result': outcome}
    #     team_schedule[i] = game_data
    #     nfl_data[team] = team_schedule

    # f.close()
    # return nfl_data
for nflteam in teams:
    teamJsonSchedule(nflteam)
pandaToJson(nfl_data, team_txt_sched, team_json_sched)