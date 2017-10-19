/* jshint esversion: 6,  loopfunc: true,  devel: true */

const url = '/elections2000/';
const candidates =  [["Dariusz Maciej GRABOWSKI", 1], ["Piotr IKONOWICZ", 2],  ["Jarosław KALINOWSKI", 3],
             ["Janusz KORWIN-MIKKE", 4],  ["Marian KRZAKLEWSKI", 5],  ["Aleksander KWAŚNIEWSKI", 6],
             ["Andrzej LEPPER", 7], ["Jan ŁOPUSZAŃSKI", 8], ["Andrzej Marian OLECHOWSKI", 9],
             ["Bogdan PAWŁOWSKI", 10], ["Lech WAŁĘSA", 11], ["Tadeusz Adam WILECKI", 12]];


function generateEmptyTable() {
    "use strict";
    let html = ``;
    for (let cn of candidates) {
        html += `
            <tr id="${cn[1]}">
                <td>${cn[0]}</td>
                <td id="votes_${cn[1]}"></td>
                <td id="percentage_${cn[1]}"></td>
                <td></td>
            </tr>
            `;
    }
    return html;
}


function addEmptyTable() {
    "use strict";
    document.querySelector('tbody').innerHTML = generateEmptyTable();
}


function fillTable(data) {
    "use strict";
    document.querySelector('h1#table_header').innerHTML = data.header;
    let receivedVotes = data.received_votes;
    let properVotes  = data.proper_votes;
    //let cards = data.cards;
    let i = 1;
    for (let candidate in receivedVotes) {
        let votes_cell = 'td#votes_' + i;
        let percentage_cell = 'td#percentage_' + i;
        let votes = receivedVotes[candidate];
        let percentage = (votes / properVotes) * 100;
        document.querySelector(votes_cell).innerHTML = votes;
        document.querySelector(percentage_cell).innerHTML = percentage.toFixed(2) + '%';
        i++;
    }

}


function updateTable(name) {
    "use strict";
    let req = new XMLHttpRequest();
    req.open('GET', `${url}${name}`);
    req.onload = function () {
        let data = JSON.parse(req.responseText);
        fillTable(data);
    };
    req.send();
}

