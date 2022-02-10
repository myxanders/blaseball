function openTab(tab) {
    document.getElementById('american').style.display = "none";
    document.getElementById('national').style.display = "none";
    document.getElementById('playoffs').style.display = "none";
    document.getElementById(tab).style.display = "block";
}


function getDivisionTeams(conf, div) {
    var div_teams = [];
    var search = Object.keys(conf);
    for (i = 0; i < search.length; i++) {
        var tm = search[i];
        if (conf[tm] == div) {
            div_teams.push(tm);
        }
    }
    return div_teams
}

function fillDivTable(table, data) {
    data.sort(function (a, b) {
        return b.pct - a.pct || a.l - b.l;
    })
    var lead_win = data[0]["w"];
    var lead_loss = data[0]["l"];
    for (i = 0; i < data.length; i++) {
        var w_diff = Math.abs(lead_win - data[i]["w"]);
        var l_diff = Math.abs(lead_loss - data[i]["l"]);
        var gb = (w_diff + l_diff) / 2;
        if (gb == 0) {
            gb = "-";
        }
        var el_num = 163 - (lead_win + data[i]["l"]);
        if (el_num < 1) {
            el_num = "E";
        }
        if (i == 0) {
            el_num = "-";
        }
        data[i]["gb"] = gb;
        data[i]["el_num"] = el_num;
    }
    data.forEach(item => {
        let row = table.insertRow();
        let team = row.insertCell(0);
        team.innerHTML = item.tm;
        let xid = item.tm.replace(' ','');
        team.id = xid;
        let record = row.insertCell(1);
        record.innerHTML = item.record;
        let pct = row.insertCell(2);
        pct.innerHTML = item.pct;
        let gb = row.insertCell(3);
        gb.innerHTML = item.gb;
        let el_num = row.insertCell(4);
        el_num.innerHTML = item.el_num;
    });
}

function fillConfTable(table, conf, leaders) {
    leaders.sort(function (a, b) {
        return b.pct - a.pct || a.l - b.l;
    })
    leaders.forEach(item => {
        let row = table.insertRow();
        let team = row.insertCell(0);
        team.innerHTML = item.tm;
        let xid = item.tm.replace(' ','');
        team.id = xid;
        let record = row.insertCell(1);
        record.innerHTML = item.record;
        let pct = row.insertCell(2);
        pct.innerHTML = item.pct;
        let gb = row.insertCell(3);
        gb.innerHTML = item.gb;
        let el_num = row.insertCell(4);
        el_num.innerHTML = item.el_num;
    });
    var outside = [];
    for (i = 0; i < conf.length; i++) {
        var tm = conf[i];
        if (leaders.includes(tm)) {
            continue;
        }
        outside.push(conf[i]);
    }

    outside.sort(function (a, b) {
        return b.pct - a.pct || a.l - b.l;
    })

    var lead_win = outside[1]["w"];
    var lead_loss = outside[1]["l"];
    for (i = 0; i < outside.length; i++) {
        var w_diff = Math.abs(lead_win - outside[i]["w"]);
        var l_diff = Math.abs(lead_loss - outside[i]["l"]);
        var gb = (w_diff + l_diff) / 2;
        var el_num = 163 - (lead_win + outside[i]["l"]);
        if (el_num < 1) {
            el_num = "E";
        }
        if (i <= 1) {
            el_num = "-";
            gb = "-";
        }
        outside[i]["gb"] = gb;
        outside[i]["el_num"] = el_num;
    }

    outside.forEach(item => {
        let row = table.insertRow();
        let team = row.insertCell(0);
        team.innerHTML = item.tm;
        let xid = item.tm.replace(' ','');
        team.id = xid;
        let record = row.insertCell(1);
        record.innerHTML = item.record;
        let pct = row.insertCell(2);
        pct.innerHTML = item.pct;
        let gb = row.insertCell(3);
        gb.innerHTML = item.gb;
        let el_num = row.insertCell(4);
        el_num.innerHTML = item.el_num;
    });

    return outside;
}
const al = {
    "NYY": "East",
    "BOS": "East",
    "TB": "East",
    "TOR": "East",
    "BAL": "East",
    "CWS": "Central",
    "DET": "Central",
    "KC": "Central",
    "MIN": "Central",
    "CLE": "Central",
    "LAA": "West",
    "HOU": "West",
    "OAK": "West",
    "TEX": "West",
    "SEA": "West"
};
const nl = {
    "ATL": "East",
    "PHI": "East",
    "NYM": "East",
    "MIA": "East",
    "WAS": "East",
    "STL": "Central",
    "CHC": "Central",
    "MIL": "Central",
    "CIN": "Central",
    "PIT": "Central",
    "LAD": "West",
    "SF": "West",
    "SD": "West",
    "ARZ": "West",
    "COL": "West"
};

function teamProfile(standings, n) {
    var tsho = standings[n]["tsho"];
    var tm = standings[n]["team"];
    var w = standings[n]["W"];
    var l = standings[n]["L"];
    var record = w + '-' + l;
    var pct = standings[n]["PCT"];
    var gb = 0;
    var el_num = 0;

    entry = {
        tsho: tsho,
        tm: tm,
        w: w,
        l: l,
        record: record,
        pct: pct,
        gb: gb,
        el_num: el_num
    }

    return entry;
}
al_standings = [];
al_leaders = [];
nl_standings = [];
nl_leaders = [];

function divTableAgg (league, div, tbl){
    var dtbl = document.getElementById(tbl);
    var dteams = getDivisionTeams(league, div);
    var dstandings = [];
    if (league == al){
        var lgstandings = al_standings;
        var lgleaders = al_leaders;
    }
    else if (league == nl){
        var lgstandings = nl_standings;
        var lgleaders = nl_leaders;
    }
    for (n = 0; n < standings.length; n++){
        if (dteams.includes(standings[n]['tsho'])){
            team = teamProfile(standings, n);
            dstandings.push(entry);
            lgstandings.push(entry);
        }
    }
    fillDivTable(dtbl, dstandings);
    lgleaders.push(dstandings[0]);
}

function confTableAgg (league, tbl){
    var ctbl = document.getElementById(tbl);
    if (league == 'al'){
        var lgstandings = al_standings;
        var lgleaders = al_leaders;
    }
    else if (league == 'nl'){
        var lgstandings = nl_standings;
        var lgleaders = nl_leaders;
    }
    fillConfTable(ctbl, lgstandings, lgleaders);
}