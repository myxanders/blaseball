function openTab(tab) {
    document.getElementById('west').style.display = "none";
    document.getElementById('east').style.display = "none";
    document.getElementById(tab).style.display = "block";
}

function fillConfTable(tbl, conf){
    var data = standings.filter(n => n.conf == conf);
    data.sort(function(a, b) {
        return b.PCT - a.PCT || a.GB - b.GB || b.tb - a.tb;
    })
    data.forEach(item => {
        let row = tbl.insertRow();
        let team = row.insertCell(0);
        team.innerHTML = item.team;
        let xid = item.team;
        xid = xid.replace(' ', '');
        if (xid == '76ers'){
            xid = 'Sixers';
        }
        team.id = xid;
        let record = row.insertCell(1);
        let wlt = item.W + '-' + item.L;
        record.innerHTML = wlt;
        let pct = row.insertCell(2);
        pct.innerHTML = item.PCT.toFixed(3);
        let gb = row.insertCell(3);
        gb.innerHTML = item.GB;
    })        
}