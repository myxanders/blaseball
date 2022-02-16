function updateWeek() {
    var wk = document.getElementById("week").value;
    document.getElementById("wk_head").innerHTML = 'Week ' + wk;
    wk = parseInt(wk);
    var slate = sched.filter(n => n.wk == wk);
    tableMaker(slate);
}

function start(){
    var slate = sched.filter(n => n.wk == 1);
    tableMaker(slate);
}

var mls_teams = {'ATL':'Atlanta Utd', 'CHI': 'Fire', 'CIN': 'Cincinnati FC', 'CLB': 'Crew', 'COL': 'Rapids', 'DAL': 'FC Dallas', 'DC': 'D.C. United', 'HOU': 'Dynamo', 'LAG': 'Galaxy', 'LFC': 'LA FC', 'MIN': 'Minnesota Utd', 'MTL': 'Impact', 'NE': 'Revolution', 'NY': 'Red Bulls', 'NYC': 'NYC FC', 'OSC': 'Orlando City', 'PHI': 'Union', 'POR': 'Timbers', 'RSL': 'Real Salt Lake', 'SEA': 'Sounders', 'SJ': 'Earthquakes', 'SKC': 'Sporting KC', 'TOR': 'Toronto FC', 'VAN': 'Whitecaps'};
function displayResults(table, data) {
    data.forEach(item => {
        let row = table.insertRow();
        let hscore = row.insertCell(0);
        hscore.innerHTML = item.homescore;
        hscore.style.fontWeight = 'bold';
        let hteam = row.insertCell(1);
        hteam.innerHTML = mls_teams[item.home];
        hteam.id = item.home;
        hteam.style.fontWeight = 'bold';
        let at = row.insertCell(2);
        at.innerHTML = 'vs.';
        let ateam = row.insertCell(3);
        ateam.innerHTML = mls_teams[item.away];
        ateam.id = item.away;
        ateam.style.fontWeight = 'bold';
        let ascore = row.insertCell(4);
        ascore.innerHTML = item.awayscore;
        ascore.style.fontWeight = 'bold';
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
    document.getElementById('west').style.display = "none";
    document.getElementById('east').style.display = "none";
    document.getElementById(tab).style.display = "block";
}


function fillConfTable(tbl, conf){
    var cstan = standings.filter(n => n.conf == conf);
    cstan.sort(function(a, b){
        return b.Pts - a.Pts || b.W - a.W || b.GD - a.GD || b.GF - a.GF;
    })
    cstan.forEach(item => {
        let row = tbl.insertRow();
        let team = row.insertCell(0);
        team.innerHTML = item.team;
        team.id = item.tsho;
        team.style.fontWeight = 'bold';
        let pts = row.insertCell(1);
        pts.innerHTML = item.Pts;
        pts.style.fontWeight = 'bold';
        let record = row.insertCell(2);
        let wlt = item.W + '-' + item.D + '-' + item.L;
        record.innerHTML = wlt;
        let gf = row.insertCell(3);
        gf.innerHTML = item.GF;
        let ga = row.insertCell(4);
        ga.innerHTML = item.GA;
        let gd = row.insertCell(5);
        gd.innerHTML = item.GD;
        let rem = row.insertCell(6);
        let gp = item.W + item.D + item.L;
        rem.innerHTML = 34 - gp;
    })       
}