function updateWeek() {
    var wk = document.getElementById("week").value;
    document.getElementById("wk_head").innerHTML = 'Week ' + wk;
    wk = parseInt(wk);
    var slate = sched.filter(n => n.week == wk);
    tableMaker(slate);
}

function start(){
    var slate = sched.filter(n => n.week == 1);
    tableMaker(slate);
}
function displayResults(table, data) {
    data.forEach(item => {
        let row = table.insertRow();
        let ascore = row.insertCell(0);
        ascore.innerHTML = item.awayscore;
        ascore.style.fontWeight = 'bold';
        let ateam = row.insertCell(1);
        if (item.awayteam == 'Niners') {
            ateam.innerHTML = '49ers';
        }
        else {
            ateam.innerHTML = item.awayteam;
        }
        ateam.id = item.awayteam;
        let at = row.insertCell(2);
        if (item.week == '21') {
            at.innerHTML = 'vs.';
        }
        else {
            at.innerHTML = '@';
        }
        let hteam = row.insertCell(3);
        hteam.innerHTML = item.hometeam;
        if (item.awayteam == 'Niners') {
            hteam.innerHTML = '49ers';
        }
        else {
            hteam.innerHTML = item.hometeam;
        }
        hteam.id = item.hometeam;
        let hscore = row.insertCell(4);
        hscore.innerHTML = item.homescore;
        hscore.style.fontWeight = 'bold';
    });
}

function clearTable(table) {
    for (x = table.rows.length - 1; x > 0; x--) {
        table.deleteRow(x);
    }
}

function tableMaker(data) {
    var tbl = document.getElementById("schedule");
    clearTable(tbl);
    displayResults(tbl, data);
}

function openTab(tab) {
    document.getElementById('NFC').style.display = "none";
    document.getElementById('AFC').style.display = "none";
    document.getElementById('playoffs').style.display = "none";
    document.getElementById(tab).style.display = "block";
}

function fillDivTable(tbl, conf, div) {
    var dstan = standings.filter(n => n.division == div && n.conference == conf);
    dstan.sort(function (a, b) {
        return b.PCT - a.PCT || b.dh2h - a.dh2h || b.d_pct - a.d_pct || b.SOV - a.SOV || b.SOS - a.SOS;
    });
    if (conf == 'AFC'){
        afc_leaders.push(dstan[0]);
    }
    else if (conf == 'NFC'){
        nfc_leaders.push(dstan[0]);
    }
    dstan.forEach(item => {
        let row = tbl.insertRow();
        let team = row.insertCell(0);
        team.innerHTML = item.Team;
        team.id = item.Team;
        let record = row.insertCell(1);
        let wlt = getRecord(item);
        record.innerHTML = wlt;
        let pct = row.insertCell(2);
        pct.innerHTML = item.PCT.toFixed(3);
        let pf = row.insertCell(3);
        pf.innerHTML = item.PF;
        let pa = row.insertCell(4);
        pa.innerHTML = item.PA;
        let pd = row.insertCell(5);
        pd.innerHTML = item.PD;
        let div = row.insertCell(6);
        div.innerHTML = item.Div;
        let conf = row.insertCell(7);
        conf.innerHTML = item.Conf;
    });
}

function fillConfTable(tbl, conf, leaders){
    leaders.sort(function (a, b) {
        return b.PCT - a.PCT || b.ch2h - a.ch2h || b.c_pct - a.c_pct || b.SOV - a.SOV || b.SOS - a.SOS;
    })
    var cstan = standings.filter(n => n.conference == conf);
    var outside = [];
    for (i = 0; i < cstan.length; i++){
        var tm = cstan[i];
        if (leaders.includes(tm)){
            continue;
        }
        outside.push(cstan[i]);
    }
    outside.sort(function(a, b) {
        return b.PCT - a.PCT || b.ch2h - a.h2h || b.dh2h - a.dh2h || b.c_pct - a.c_pct || b.SOV - a.SOV || b.SOS - a.SOS;
    })

    leaders.forEach(item => {
        let row = tbl.insertRow();
        let team = row.insertCell(0);
        team.innerHTML = item.Team;
        team.id = item.Team;
        let record = row.insertCell(1);
        let wlt = getRecord(item);
        record.innerHTML = wlt;
        let pct = row.insertCell(2);
        pct.innerHTML = item.PCT.toFixed(3);
        let pf = row.insertCell(3);
        pf.innerHTML = item.PF;
        let pa = row.insertCell(4);
        pa.innerHTML = item.PA;
        let pd = row.insertCell(5);
        pd.innerHTML = item.PD;
        let conf = row.insertCell(6);
        conf.innerHTML = item.Conf;
        let sov = row.insertCell(7);
        sov.innerHTML = item.SOV.toFixed(3);
        let sos = row.insertCell(8);
        sos.innerHTML = item.SOS.toFixed(3);
    })
    outside.forEach(item => {
        let row = tbl.insertRow();
        let team = row.insertCell(0);
        team.innerHTML = item.Team;
        team.id = item.Team;
        let record = row.insertCell(1);
        let wlt = getRecord(item);
        record.innerHTML = wlt;
        let pct = row.insertCell(2);
        pct.innerHTML = item.PCT.toFixed(3);
        let pf = row.insertCell(3);
        pf.innerHTML = item.PF;
        let pa = row.insertCell(4);
        pa.innerHTML = item.PA;
        let pd = row.insertCell(5);
        pd.innerHTML = item.PD;
        let conf = row.insertCell(6);
        conf.innerHTML = item.Conf;
        let sov = row.insertCell(7);
        sov.innerHTML = item.SOV.toFixed(3);
        let sos = row.insertCell(8);
        sos.innerHTML = item.SOS.toFixed(3);
    })        
}

function getRecord(item) {
    var wlt = item.W + '-' + item.L
    if (item.t > 0) {
        wlt = wlt + '-' + item.T
    }
    return wlt;
}

var afc_leaders = [];
var nfc_leaders = [];