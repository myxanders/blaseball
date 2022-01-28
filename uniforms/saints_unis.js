function endDates() {
    var e = document.getElementById("startYear");
    var x = parseInt(e.value);
    endOptions(x);
}

function endOptions(year) {
    var n = document.getElementById('endYear');
    clearOptions(n);
    for (i = year; i <= 2021; i++) {
        var opt = document.createElement('option');
        opt.value = i;
        opt.innerHTML = i;
        n.append(opt);
    }
}

function clearOptions(sel) {
    var i, s = sel.options.length - 1;
    for (i = s; i >= 0; i--) {
        sel.remove(i);
    }
}

function createCriterion() {
    var start = document.getElementById("startYear").value;
    var end = document.getElementById("endYear").value;
    var weeks = document.getElementById("gameType").value;
    var day = document.getElementById("gameDay").value;
    var network = document.getElementById("network").value;
    var location = document.getElementById("location").value;
    var opponent = document.getElementById("opponent").value;
    var uni_set = document.getElementById("uniSet").value;
    var jersey = document.getElementById("jersey").value;
    var pants = document.getElementById("pants").value;

    criteria = {
        start: start,
        end: end,
        weeks: weeks,
        day: day,
        network: network,
        location: location,
        opponent: opponent,
        uni_set: uni_set,
        jersey: jersey,
        pants: pants
    }
    updateImg(criteria);
    fetchResults(criteria);
}

function updateImg(criteria) {
    var mannequin = document.getElementById("uniPreview");
    var src_img = '';
    if (criteria.uni_set == 'Throwback') {
        mannequin.src = "tb.png";
    }
    else if (criteria.uni_set == 'Color Rush') {
        mannequin.src = "cr.png";
    }
    else {
        if (criteria.jersey == 'black') {
            src_img += 'b';
        }
        else if (criteria.jersey == 'white') {
            src_img += 'w';
        }
        if (criteria.pants == 'black') {
            src_img += 'b';
        }
        else if (criteria.pants == 'gold') {
            src_img += 'g';
        }
        else if (criteria.pants == 'white') {
            src_img += 'w';
        }
        if (criteria.pants == 'All'){
            src_img += '_top';
        }
        if (criteria.jersey == 'All'){
            src_img += '_bot';
        }
        if (criteria.jersey == 'All' && criteria.pants == 'All'){
            src_img = 'bg'
        }
        src_img += '.png';

        mannequin.src = src_img;
    }
}

function fetchResults(criteria) {
    var results = unis.filter(n => n.year >= criteria.start && n.year <= criteria.end);
    if (criteria.network != "All") {
        results = results.filter(n => n.network == criteria.network);
    }
    if (criteria.weeks != "All") {
        if (criteria.weeks == "Regular") {
            results = results.filter(n => n.week < 20);

        }
        else if (criteria.weeks == "Playoffs") {
            results = results.filter(n => n.week >= 20);
        }
    }
    if (criteria.opponent != "All") {
        results = results.filter(n => n.opp == criteria.opponent);
    }
    if (criteria.day != "A") {
        results = results.filter(n => n.day == criteria.day);
    }
    if (criteria.uni_set != "All") {
        results = results.filter(n => n.uni_type == criteria.uni_set);
    }
    if (criteria.location != "All") {
        results = results.filter(n => n.game_site == criteria.location);
    }
    if (criteria.jersey != "All") {
        results = results.filter(n => n.tops == criteria.jersey);
    }
    var pants_color = criteria.pants;
    var rec = document.getElementById("record");
    if (criteria.pants != "All") {
        results = results.filter(n => n.bottoms == criteria.pants);
        if (criteria.pants == "gold") {
            pants_color = "#D3BC8D";
        }
    }
    else if (criteria.uni_set == "Color Rush") {
        pants_color = "white";
    }
    else if (criteria.uni_set == "Throwback") {
        pants_color = "goldenrod";
    }
    else {
        pants_color = "black";
    }
    rec.style.color = pants_color;
    getRecord(results);
    tableMaker(results);
}

function getRecord(data) {
    var wins = 0;
    var losses = 0;
    var ties = 0;
    var pf = 0;
    var pa = 0;
    var pd = 0;
    for (var i = 0; i < data.length; i++) {
        if (data[i].result == "W") {
            wins++;
        }
        else if (data[i].result == "L") {
            losses++;
        }
        else if (data[i].result == "T") {
            ties++;
        }
        pf = pf + data[i].pf;
        pa = pa + data[i].pa;

    }
    var rec = document.getElementById("record");
    var mov = document.getElementById("scoring");
    var record = wins + '-' + losses;
    if (ties > 0) {
        record = record + '-' + ties;
    }
    var gp = wins + losses + ties;
    if (gp == 0) {
        gp = 1;
    }
    var pct = (wins + (.5 * ties)) / gp;
    var pfpg = (pf / gp).toFixed(2);
    var papg = (pa / gp).toFixed(2);
    pct = pct.toFixed(3);
    record = record + ' (' + pct + '%)'
    var margin = parseFloat(pfpg) + ' - ' + parseFloat(papg);
    if (pfpg - papg >= 3) {
        mov.style.color = "darkgreen";
    }
    else if (pfpg - papg <= -3) {
        mov.style.color = "darkred";
    }
    else {
        mov.style.color = "black";
    }
    rec.innerHTML = record;
    mov.innerHTML = margin;
}

function displayResults(table, data) {
    data.sort(function (a, b) {
        return b.year - a.year || b.week - a.week;
    })
    data.forEach(item => {
        if (item.day == "S") {
            gameday = "Sunday";
        }
        else if (item.day == "M") {
            gameday = "Monday";
        }
        else if (item.day == "R") {
            gameday = "Thursday";
        }
        else if (item.day == "F") {
            gameday = "Friday";
        }
        else if (item.day == "D") {
            gameday = "Saturday";
        }

        if (item.week == 20) {
            gameweek = "Wild Card";
        }
        else if (item.week == 21) {
            gameweek = "Divisional";
        }
        else if (item.week == 22) {
            gameweek = "NFCCG";
        }
        else if (item.week == 23) {
            gameweek = "Super Bowl";
        }
        else {
            gameweek = item.week;
        }
        let row = table.insertRow();
        let year = row.insertCell(0);
        year.innerHTML = item.year;
        let week = row.insertCell(1);
        week.innerHTML = gameweek;
        let day = row.insertCell(2);
        day.innerHTML = gameday;
        let opp = row.insertCell(3);
        opp.innerHTML = item.opp;
        let game_site = row.insertCell(4);
        game_site.innerHTML = item.game_site;
        let uni_set = row.insertCell(5);
        uni_set.innerHTML = item.uni_type;
        let tops = row.insertCell(6);
        tops.style.backgroundColor = item.tops;
        let bottoms = row.insertCell(7);
        if (item.bottoms == "gold") {
            if (item.uni_type == "Normal") {
                bottom_color = "#D3BC8D";
            }
            else if (item.uni_type == "Throwback") {
                bottom_color = "goldenrod";
            }
        }
        else {
            bottom_color = item.bottoms;
        }
        bottoms.style.backgroundColor = bottom_color;
        bottoms.style.borderLeft = "1px solid grey";
        let result = row.insertCell(8);
        result.innerHTML = item.result;
        var game_score = item.pf + '-' + item.pa;
        if (item.OT == 1) {
            game_score = game_score + ' (OT)';
        }
        let score = row.insertCell(9);
        score.innerHTML = game_score;
        let network = row.insertCell(10);
        network.innerHTML = item.network;
    });
}

function clearTable(table) {
    for (x = table.rows.length - 1; x > 0; x--) {
        table.deleteRow(x);
    }
}

function tableMaker(data) {
    var tbl = document.getElementById("data");
    clearTable(tbl);
    displayResults(tbl, data);

}