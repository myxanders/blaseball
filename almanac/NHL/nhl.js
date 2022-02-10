function openTab(tab) {
    document.getElementById('western').style.display = "none";
    document.getElementById('eastern').style.display = "none";
    document.getElementById('westplayoffs').style.display = "none";
    document.getElementById('eastplayoffs').style.display = "none";
    document.getElementById(tab).style.display = "block";
}

west_standings = [];
east_standings = [];
west_wc = [];
east_wc = [];
west_lead = [];
east_lead = [];

function fillDivTable(table, data, outside, leaders) {
    data.sort(function (a, b) {
        return b.pts - a.pts || b.pp - a.pp || b.w - a.w || b.r_ow - a.r_ow || b.gd - a.gd || b.gf - a.gf;
    })

    for (i = 0; i < data.length; i++) {
        if (i <= 2) {
            leaders.push(data[i]);
        }
        else if (i > 2) {
            outside.push(data[i]);
        }
    }
    data.forEach(item => {
        let row = table.insertRow();
        let tm = row.insertCell(0);
        tm.innerHTML = item.tm;
        var xid = item.tm.replace(' ', '');
        tm.id = xid;
        let record = row.insertCell(1);
        record.innerHTML = item.record;
        let pts = row.insertCell(2);
        pts.innerHTML = item.pts;
        pts.style.fontWeight = 'bold';
        let r_ow = row.insertCell(3);
        r_ow.innerHTML = item.r_ow;
        let gf = row.insertCell(4);
        gf.innerHTML = item.gf;
        let ga = row.insertCell(5);
        ga.innerHTML = item.ga;
        let gd = row.insertCell(6);
        gd.innerHTML = item.gd;
        let pp = row.insertCell(7);
        pp.innerHTML = item.pp;
        let gr = row.insertCell(8);
        gr.innerHTML = item.gr;
    });
}

function fillConfTable(table, conf) {
    conf.sort(function (a, b) {
        return b.pts - a.pts || b.pp - a.pp || b.w - a.w || b.r_ow - a.r_ow || b.gd - a.gd || b.gf - a.gf;
    })
    conf.forEach(item => {
        let row = table.insertRow();
        let tm = row.insertCell(0);
        tm.innerHTML = item.tm;
        var xid = item.tm.replace(' ', '');
        tm.id = xid;
        let record = row.insertCell(1);
        record.innerHTML = item.record;
        let pts = row.insertCell(2);
        pts.innerHTML = item.pts;
        pts.style.fontWeight = 'bold';
        let r_ow = row.insertCell(3);
        r_ow.innerHTML = item.r_ow;
        let gf = row.insertCell(4);
        gf.innerHTML = item.gf;
        let ga = row.insertCell(5);
        ga.innerHTML = item.ga;
        let gd = row.insertCell(6);
        gd.innerHTML = item.gd;
        let pp = row.insertCell(7);
        pp.innerHTML = item.pp;
        let gr = row.insertCell(8);
        gr.innerHTML = item.gr;
    });

    return conf;
}

function teamProfile(standings, n) {
    var tm = standings[n]["team"];
    var w = standings[n]["W"];
    var l = standings[n]["L"];
    var otl = standings[n]["OTL"];
    var record = w + '-' + l + '-' + otl;
    var pts = standings[n]["PTS"];
    var r_ow = standings[n]["ROW"];
    var gf = standings[n]["GF"];
    var ga = standings[n]["GA"];
    var gd = gf - ga;
    var gp = w + l + otl
    var gr = 82 - gp;
    var pp = pts / (2 * gp);
    var div = standings[n]["div"];
    pp = pp.toFixed(3);

    entry = {
        tm: tm,
        w: w,
        l: l,
        otl: otl,
        record: record,
        pts: pts,
        pp: pp,
        r_ow: r_ow,
        gf: gf,
        ga: ga,
        gd: gd,
        gr: gr,
        div: div
    }

    return entry;
}

function divTableAgg(tbl, div) {
    var dtbl = document.getElementById(tbl);
    var dstandings = [];
    if (div == 'Atlantic' || div == 'Metropolitan') {
        var cstandings = east_standings;
        var wc_race = east_wc;
        var lead_race = east_lead;
    }
    else if (div == 'Central' || div == 'Pacific') {
        var cstandings = west_standings;
        var wc_race = west_wc;
        var lead_race = west_lead;
    }
    var newdata = standings.filter(n => n.div == div);
    for (i = 0; i < newdata.length; i++) {
        team = teamProfile(newdata, i);
        cstandings.push(team);
        dstandings.push(team);
    }
    fillDivTable(dtbl, dstandings, wc_race, lead_race);
}

function confTableAgg(tbl1, tbl2, wctbl, conf, leaders, wc) {
    if (conf == 'West') {
        var div1 = 'Central';
        var div2 = 'Pacific';
    }
    else if (conf == 'East') {
        var div1 = 'Atlantic';
        var div2 = 'Metropolitan';
    }
    var div_1_lead = document.getElementById(tbl1);
    var div_2_lead = document.getElementById(tbl2);
    var conf_wc_race = document.getElementById(wctbl);
    console.log(leaders);
    var div_1_teams = leaders.filter(n => n.div == div1);
    var div_2_teams = leaders.filter(n => n.div == div2);
    fillConfTable(div_1_lead, div_1_teams);
    fillConfTable(div_2_lead, div_2_teams);
    fillConfTable(conf_wc_race, wc);
}