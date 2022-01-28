def pandaToJson(data, txt, json):
    with open(txt, "w") as f:
        f.write(str(data))

    fin = open(txt, "rt")
    fout = open(json, "wt")

    for line in fin:
        fout.write(line.replace("'", '"'))
    
    fin.close()
    fout.close()

def removeBattingTwins(df):
    df['feedback'] = df['name'].duplicated()
    bat_cols = ['name','tsho','PA', 'H', 'BB', 'SACH', 'SACF', 'SO', 'CS', 'R', 'RBI', 'HR', 'GP']
    fb = df[df.feedback == True].sort_values('name').drop_duplicates(subset=['name'])
    n = fb.shape[0]
    i = 0
    while i < n:
        twin = fb.iloc[i]['name']
        beep = df[df.name == twin]
        tms = '/'.join(beep['tsho'])
        df.loc[df['name'].map(lambda x: x == twin), 'tsho'] = tms
        for col in bat_cols:
            if col in ('name', 'tsho'):
                continue
            total = beep[col].sum()
            df.loc[df.name == twin, col] = total 
        i += 1
    df.drop_duplicates(subset='name', inplace=True)
    df = df[bat_cols]
    #target = gms
    #df = df[df['PA'] >= target]
    df = df[df['PA'] > 99]
    return df
    

def removePitchingTwins(df):
    df['feedback'] = df['name'].duplicated()
    bat_cols = ['name','tsho','IP', 'K', 'BB', 'H', 'RA', 'HR', 'QS', 'GP']
    fb = df[df.feedback == True].sort_values('name').drop_duplicates(subset=['name'])
    n = fb.shape[0]
    i = 0
    while i < n:
        twin = fb.iloc[i]['name']
        beep = df[df.name == twin]
        tms = '/'.join(beep['tsho'])
        df.loc[df['name'].map(lambda x: x == twin), 'tsho'] = tms
        for col in bat_cols:
            if col in ('name', 'tsho'):
                continue
            total = beep[col].sum()
            df.loc[df.name == twin, col] = total 
        i += 1
    df.drop_duplicates(subset='name', inplace=True)
    df = df[bat_cols]
    #target = .8 * gms
    #df = df[df['IP'] >= target]
    df = df[df['IP'] > 79]
    return df

def advBatting(df):
    df['aOBP'] = round((df['H'] + df['BB'] + df['SACH'] + df['SACF'])/df['PA'], 3)
    df['DEAD'] = round((df['SO'] + df['CS'])/df['PA'], 3)
    df['PM'] = round(df['aOBP'] - df['DEAD'], 3)
    df['RM'] = round((df['R'] + df['RBI'] - df['HR'])/df['PA'], 3)
    df['IMP'] = round(df['RM']/df['aOBP'], 3)

def advPitching(df):
    df['KIP'] = round(df['K']/df['IP'], 3)
    df['WHIP'] = round((df['BB'] + df['H'])/df['IP'], 3)
    df['NET'] = round(df['KIP'] - df['WHIP'], 3)
    df['QS%'] = round(df['QS']/df['GP'], 3)

def remove_zeros(number):
    while number % 10 == 0:
        number //= 10
    return number    