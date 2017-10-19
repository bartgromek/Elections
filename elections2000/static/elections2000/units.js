/* jshint esversion: 6,  loopfunc: true,  devel: true */
//const url = '/elections2000/';

function division(name) {
    "use strict";
    let req = new XMLHttpRequest();
    req.open('GET', `/elections2000/${name}`);
    req.onload = function () {
        let data = JSON.parse(req.responseText);
        addUnits(data);
    };
    req.send();
}

function addUnits(data) {
    "use strict";
    let html = `<ul class="list-group">`;
    if (data.length) {
        html += `<h2>Header</h2>`;
        for (let i = 0; i < data.length; i++) {
            html += `<li><button>${data[i].name}</button></li>
`;
        }
        html += `</ul>`;
    }
    document.querySelector('div#division').innerHTML = html;
}