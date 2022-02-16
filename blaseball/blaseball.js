function ILBTeams() {
    let shorts = ['KCBM', 'CRAB', 'DALE', 'CHI', 'BOS', 'FRI', 'ATL', 'SEA', 'JAZZ', 'LIFT', 'LVRS', 'YELL', 'CORE', 'NYM', 'CAN', 'PIES', 'CHST', 'SPY', 'STK', 'HELL', 'TGRS', 'TACO', 'CDMX', 'OHWO'];
    let names = ['The Breath Mints', 'Crabs', 'Dale', 'Firefighters', 'Flowers', 'Fridays', 'Georgias', 'Garages', 'Jazz Hands', 'Lift', 'Lovers', 'Magic', 'Mechanics', 'Millennials', 'Moist Talkers', 'Pies', 'Shoe Thieves', 'Spies', 'Steaks', 'Sunbeams', 'Tigers', 'Unlimited Tacos', 'Wild Wings', 'Worms'];
    let emojis = ['0x1F36C', '0x1F980', '0x1F6A4', '0x1F525', '0x1F337', '0x1F3DD', '0x1F531', '0x1F3B8', '0x1F450', '0x1F3CB', '0x1F48B', '0x2728', '0x1F6E0', '0x1F4F1', '0x1F5E3', '0x1F967', '0x1F45F', '0x1F575', '0x1F969', '0x1F31E', '0x1F405', '0x1F32E', '0x1F357', '0x1F40C'];
    var n = document.getElementById('team');
    for (i = 0; i < 24; i++) {
        var opt = document.createElement('option');
        opt.value = shorts[i];
        opt.innerHTML = String.fromCodePoint(emojis[i]) + " " + names[i];
        n.append(opt);
    }

}

function chooseSzn() {
    var e = document.getElementById("year");
    var szn = e.value;
    sznData(szn);
}

function sznData(year) {
    var batters = bats[year];
    var pitchers = arms[year];
    var filter = document.getElementById("team").value;
    var b_tbl = document.getElementById("batting_data");
    var p_tbl = document.getElementById("pitching_data");
    b_tbl.className = 'table';
    p_tbl.className = 'table';
    if (filter != 'All') {
        batters = batters.filter(n => n.tsho.includes(filter));
        b_tbl.className += " " + filter;
        pitchers = pitchers.filter(n => n.tsho.includes(filter));
        p_tbl.className += " " + filter;
    }        
    clearTable(b_tbl);
    clearTable(p_tbl);
    displayBattingResults(b_tbl, batters);
    displayPitchingResults(p_tbl, pitchers)
}

function start() {
    ILBTeams();
    sznData('season23');
}

function clearTable(table) {
    for (x = table.rows.length - 1; x > 0; x--) {
        table.deleteRow(x);
    }
}

function displayBattingResults(table, data) {
    data.sort(function (a, b) {
        return a.Rank - b.Rank || a.name - b.name;
    })
    data.forEach(item => {
        let row = table.insertRow();
        let rank = row.insertCell(0);
        rank.innerHTML = item.Rank;
        let player = row.insertCell(1);
        if (item.name == 'Jos� Haley' || item.name == 'Samothes Demb�l�'){
            item.name = item.name.replace(/\uFFFD/g, 'é');
        }
        if (item.name == 'Ra�l Leal' || item.name == 'Jes�s Koch'){
            item.name = item.name.replace(/\uFFFD/g, 'ú');
        }
        if (item.name == 'Yrj� Kerfuffle'){
            item.name = item.name.replace(/\uFFFD/g, 'ö');
        }
        player.innerHTML = item.name;
        let team = row.insertCell(2);
        team.innerHTML = item.tsho;
        let rating = row.insertCell(3);
        rating.innerHTML = item.Rating.toFixed(3);
        let pm = row.insertCell(4);
        pm.innerHTML = item.PM.toFixed(3);
        let rm = row.insertCell(5);
        rm.innerHTML = item.RM.toFixed(3);
        let imp = row.insertCell(6);
        imp.innerHTML = item.IMP.toFixed(3);
        let aobp = row.insertCell(7);
        aobp.innerHTML = item.aOBP.toFixed(3);
        let dead = row.insertCell(8);
        dead.innerHTML = item.DEAD.toFixed(3);
    });
}

function displayPitchingResults(table, data) {
    data.sort(function (a, b) {
        return b.Rating - a.Rating || a.name - b.name;
    })
    data.forEach(item => {
        let row = table.insertRow();
        let rank = row.insertCell(0);
        rank.innerHTML = item.Rank;
        let player = row.insertCell(1);
        player.innerHTML = item.name;
        let team = row.insertCell(2);
        team.innerHTML = item.tsho;
        let rating = row.insertCell(3);
        rating.innerHTML = item.Rating.toFixed(3);
        let net = row.insertCell(4);
        net.innerHTML = item.NET.toFixed(3);
        let qs = row.insertCell(5);
        qs.innerHTML = item['QS%'].toFixed(3);
        let fip = row.insertCell(6);
        fip.innerHTML = item.FIP.toFixed(3);
        let kip = row.insertCell(7);
        kip.innerHTML = item.KIP.toFixed(3);
        let whip = row.insertCell(8);
        whip.innerHTML = item.WHIP.toFixed(3);
    });
}

function toggleBatters() {
    var p = document.getElementById("pitching_table");
    p.style.display = "none";
    var pb = document.getElementById("pitching_btn");
    pb.className = pb.className.replace(" active", "");

    var b = document.getElementById("batting_table");
    b.style.display = "block";
    var bb = document.getElementById("batting_btn");
    bb.className += " active";
}

function togglePitchers() {
    var b = document.getElementById("batting_table");
    b.style.display = "none";
    var bb = document.getElementById("batting_btn");
    bb.className = bb.className.replace(" active", "");

    var p = document.getElementById("pitching_table");
    p.style.display = "block";
    var pb = document.getElementById("pitching_btn");
    pb.className += " active";
}