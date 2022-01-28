import requests
import json
import pandas as pd
# import sys
import time
from variables import bats_json_file, arms_json_file, arms_helper, bats_helper
from config import pandaToJson, removeBattingTwins, removePitchingTwins, advBatting, advPitching
import urllib
import math

checkpoints = {
    "Earlsiesta": 27,
    "Midseason": 50,
    "Latesiesta": 72,
    "Endseason": 99
}

tids = ["105bc3ff-1320-4e37-8ef0-8d595cb95dd0", "23e4cbc1-e9cd-47fa-a35b-bfa06f726cb7", "36569151-a2fb-43c1-9df7-2df512424c82", "3f8bbb15-61c0-4e3f-8e4a-907a5fb1565e", "57ec08cc-0411-4643-b304-0e80dbc15ac7", "747b8e4a-7e50-4638-a973-ea7950a3e739", "7966eb04-efcc-499b-8f03-d13916330531", "878c1bf6-0d21-4659-bfee-916c8314d69c", "979aee4a-6d80-4863-bf1c-ee1a78e06024", "9debc64f-74b7-4ae1-a4d6-fce0144b6ea5", "a37f9158-7f82-46bc-908c-c9e2dda7c33b", "adc5b394-8f76-416d-9ce9-813706877b84", "b024e975-1c4a-4575-8936-a3754a08806a",
        "b63be8c2-576a-4d6e-8daf-814f8bcea96f", "b72f3061-f573-40d7-832a-5ad475bd7909", "bfd38797-8404-4b38-8b82-341da28b1f83", "ca3f1c8c-c025-4d8e-8eef-5be6accbeb16", "eb67ae5e-c4bf-46ca-bbbc-425cd34182ff", "f02aeae2-5e6a-4098-9842-02d2273f25c7", "8d87c468-699a-47a8-b40d-cfb73a5660ad", "c73b705c-40ad-4633-a6ed-d357ee2e2bcf", "d9f89a8a-c563-493e-9d64-78e4f9a55d4a", "46358869-dce9-4a01-bfba-ac24fc56f57e", "bb4a9de5-c924-4923-a0cb-9d1445f1ee5d", "47df036-3aa4-4b98-8e9e-fe1d3ff1894b", "2e22beba-8e36-42ba-a8bf-975683c52b5f"]
jazz = "a37f9158-7f82-46bc-908c-c9e2dda7c33b"


def update_stats(point, szn):
    batting_data = []
    pitching_data = []
    print("Gathering data for ", point, szn, "...")
    query_szn = str(int(szn) - 1)
    for team in tids:
        api_call = "https://api.blaseball-reference.com/v2/stats?type=season&group=hitting%2Cpitching&season=" + \
            query_szn + "&gameType=R&teamId=" + team
        # df = pd.read_json(api_call)
        f = urllib.request.urlopen(api_call)
        data = json.load(f)
        f.close()
        b_size = len(data[0]['splits'])
        p_size = len(data[1]['splits'])
        i = 0
        j = 0
        while i < b_size:
            pa = data[0]['splits'][i]['stat']['plate_appearances']
            hits = data[0]['splits'][i]['stat']['hits']
            bb = data[0]['splits'][i]['stat']['walks']
            sacb = data[0]['splits'][i]['stat']['sacrifice_bunts']
            sacf = data[0]['splits'][i]['stat']['sacrifice_flies']
            so = data[0]['splits'][i]['stat']['strikeouts']
            cs = data[0]['splits'][i]['stat']['caught_stealing']
            r = data[0]['splits'][i]['stat']['runs']
            rbi = data[0]['splits'][i]['stat']['runs_batted_in']
            hr = data[0]['splits'][i]['stat']['home_runs']
            fullname = data[0]['splits'][i]['player']['fullName']
            fullname = fullname.replace("'", "`")
            if fullname == 'Jes�s Koch':
                fullname = 'Jesús Koch'
            if fullname == 'Jos� Haley':
                fullname = 'José Haley'
            if fullname == 'Ra�l Leal':
                fullname = 'Raúl Leal'
            if fullname == 'Yrj� Kerfuffle':
                fullname = 'Yrjö Kerfuffle'
            if fullname == 'Samothes Demb�l�':
                fullname = 'Samothes Dembélé'

            batter = {
                'name': fullname,
                'tsho': data[0]['splits'][i]['team']['team_abbreviation'],
                'PA': pa,
                'H': hits,
                'BB': bb,
                'SACH': sacb,
                'SACF': sacf,
                'SO': so,
                'CS': cs,
                'R': r,
                'RBI': rbi,
                'HR': hr,
                'GP': data[0]['splits'][i]['stat']['appearances'],
            }
            batting_data.append(batter)
            i += 1
        while j < p_size:
            raw_ip = data[1]['splits'][j]['stat']['innings']
            leftover = raw_ip - math.floor(raw_ip)
            ip = math.floor(raw_ip) + (33 * leftover)
            k = data[1]['splits'][j]['stat']['strikeouts']
            bb = data[1]['splits'][j]['stat']['walks']
            ha = data[1]['splits'][j]['stat']['hits_allowed']
            qs = data[1]['splits'][j]['stat']['quality_starts']
            gp = data[1]['splits'][j]['stat']['games']
            ra = data[1]['splits'][j]['stat']['runs_allowed']
            fullname = data[1]['splits'][j]['player']['fullName']
            fullname = fullname.replace("'", "`")

            pitcher = {
                'name': fullname,
                'tsho': data[1]['splits'][j]['team']['team_abbreviation'],
                'rawIP': round(raw_ip, 1),
                'IP': round(ip, 2),
                'K': k,
                'BB': bb,
                'H': ha,
                'RA': ra,
                'HR': data[1]['splits'][j]['stat']['home_runs_allowed'],
                'QS': qs,
                'GP': gp
            }
            pitching_data.append(pitcher)
            j += 1

    print("Data export complete.")
    time.sleep(2)
    return batting_data, pitching_data


def pitchingNormalize(data, szn):
    dataset = pd.DataFrame(data)
    df = removePitchingTwins(dataset)
    advPitching(df)
    stats = {}
    lgHR = df['HR'].sum()
    lgBB = df['BB'].sum()
    lgIP = df['IP'].sum()
    lgERA = round((9 * df['RA'].sum()) / lgIP, 2)
    FIP_const = round(lgERA - (((13 * lgHR) + (3 * lgBB)) / lgIP), 3)
    df['ERA'] = round(((9 * df['RA']) / df['IP']), 2)
    df['FIP'] = round(((13 * df['HR'])+(3 * df['BB']) -
                      (2 * df['K'])) / df['IP'] + FIP_const, 3)
    df['NET_norm'] = round((df['NET']-df['NET'].min()) /
                           (df['NET'].max()-df['NET'].min()), 4)
    df['QS%_norm'] = round((df['QS%']-df['QS%'].min()) /
                           (df['QS%'].max()-df['QS%'].min()), 4)
    df['FIP_norm'] = 1 - \
        round((df['FIP']-df['FIP'].min())/(df['FIP'].max()-df['FIP'].min()), 4)
    df['Rating'] = round(df['NET_norm'] + df['QS%_norm'] + df['FIP_norm'], 4)
    df['Rank'] = df['Rating'].rank(method='min', ascending=False)
    df['RA'] = round(df['RA'], 1)
    df.fillna(0)
    jsdf = df.to_json(orient='records')
    season = 'season' + szn
    stats[season] = json.loads(jsdf)
    pandaToJson(stats, arms_helper, arms_json_file)


def battingNormalize(data, szn):
    dataset = pd.DataFrame(data)
    df = removeBattingTwins(dataset)
    advBatting(df)
    stats = {}
    df['PM_norm'] = round((df['PM']-df['PM'].min()) /
                          (df['PM'].max()-df['PM'].min()), 4)
    df['RM_norm'] = round((df['RM']-df['RM'].min()) /
                          (df['RM'].max()-df['RM'].min()), 4)
    df['IMP_norm'] = round((df['IMP']-df['IMP'].min()) /
                           (df['IMP'].max()-df['IMP'].min()), 4)
    df['Rating'] = round(df['PM_norm'] + df['RM_norm'] + df['IMP_norm'], 4)
    df.fillna(0)
    df['Rank'] = df['Rating'].rank(method='min', ascending=False)
    df['RBI'] = round(df['RBI'], 1)
    jsdf = df.to_json(orient='records')
    season = 'season' + szn
    stats[season] = json.loads(jsdf)
    pandaToJson(stats, bats_helper, bats_json_file)


def writeToJson(data, file):
    with open(file, 'w') as dest:
        dest.write(json.dumps(data))


def re_check_point(point, szn):
    print(point, " is not a valid input.")
    new_point = input(
        "Please use a season checkpoint (Earlsiesta, Midseason, Latesiesta, Endseason). ")
    if new_point in checkpoints:
        tables = update_stats(new_point, szn)
        battingNormalize(tables[0], szn)
        pitchingNormalize(tables[1], szn)

    else:
        re_check_point(new_point, szn)


if __name__ == '__main__':
    point, szn = input(
        "What update are you going for (Earlsiesta, Midseason, Latesiesta, Endseason) and what season? ").split()
    if point in checkpoints:
        tables = update_stats(point, szn)
        battingNormalize(tables[0], szn)
        pitchingNormalize(tables[1], szn)

    else:
        re_check_point(point, szn)
