/**
 * Created by Bartg1 on 05.05.2017.
 */

// jshint esversion: 6,  loopfunc: true,  devel: true

const candidates =  ["Dariusz Maciej GRABOWSKI", "Piotr IKONOWICZ", "Jarosław KALINOWSKI",
             "Janusz KORWIN-MIKKE", "Marian KRZAKLEWSKI", "Aleksander KWAŚNIEWSKI",
             "Andrzej LEPPER", "Jan ŁOPUSZAŃSKI", "Andrzej Marian OLECHOWSKI",
             "Bogdan PAWŁOWSKI", "Lech WAŁĘSA", "Tadeusz Adam WILECKI"];

const url = '/wybory2000/';

function giveUsername() {
    return new Promise(function (resolve) {
        let req = new XMLHttpRequest();
        req.onload = function () {
            let data = JSON.parse(req.responseText);
            resolve(data);
        };
        req.open('GET', url + 'nazwa_uz.json');
        req.send();
    });
}


function logged(login) {
    return (login !== undefined && login !== '');
}


document.addEventListener("DOMContentLoaded", function () {
    giveUsername().then(function (resolve) {
        if (!logged(resolve)) {
            document.querySelector('div.wylogowanie').style.display = 'none'; // user is logged
        } else {
            document.querySelector('div.logowanie').style.display = 'none';
        }
    });
});

function updateWrapper(name) {
    giveUsername().then(function (resolve) {
        update(name, resolve);
    });
}

function update(name, login) {
    updateOffspring(name);
    updateTable(name, login);
}

function updateButtons() {
    document.querySelector('div.map').style.display = 'none';
    document.querySelector('div.potomstwo').style.display = 'inline';
    let buttons = document.querySelectorAll('button.potomstwo');
    for (let i = 0; i < buttons.length; i++) {
        let buttonClass = buttons[i].id;
        buttons[i].onclick = function () {
            updateWrapper(buttonClass);
        };
    }
}

//document.querySelector('div.gminy').style.display = 'none';

function updateTable(name, login) {
    let req = new XMLHttpRequest();
    req.open('GET', `${url}${name}.json`);
    req.onload = function () {
        let data = JSON.parse(req.responseText);
        localStorage.setItem('table', JSON.stringify(data));
        let html = ``;
        html += generateTable(data, login);
        document.querySelector('div.table').innerHTML = html;
    };
    req.send();
}

function updateOffspring(name) {
    let req = new XMLHttpRequest();
    req.open('GET', `${url}${name}/pot.json`);
    req.onload = function () {
        let data = JSON.parse(req.responseText);
        localStorage.setItem('offspring', JSON.stringify(data));
        document.querySelector('div.potomstwo').innerHTML = offspring(data);
        updateButtons();
    };
    req.send();
}




function offspring(data) {
    let html = ``;
    if (data.length) {
        html = `<h1>Wyniki w  podległych jednostkach</h1>`;
        for (let i = 0; i < data.length; i++) {
            html += `<li><button class="potomstwo" type="button" id="${data[i].skrót}${data[i].pk}">${data[i].nazwa}</button></li>
`;
        }
    }
    return html;
}

function search() {
    document.querySelector('div.gminy').style.display = 'inline';
    let input = document.querySelector('input#gmina').value;
    let req = new XMLHttpRequest();
    req.open('GET', `${url}gmina/${input}.json`);
    req.onload = function () {
        let data = JSON.parse(req.responseText);
        document.querySelector('div.tabela').innerHTML = "";
        document.querySelector('div.potomstwo').innerHTML = "";
        let html = `<h1 id="id_search_results"> Gminy zawierające frazę: ${input} </h1>`;
        for (let i = 0; i < data.length; i++) {
            html += `<li><button class="potomstwo" id="${data[i].skrót}${data[i].pk}">${data[i].nazwa}</button></li>
    `;
        }
        document.querySelector('div.gminy').innerHTML = html;
        updateButtons();
    };
    req.send();

}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function enableEdit(candidate, wnPk, obwPk, og, wk, wg) {
    console.log(candidate);
    document.querySelector('div.dynamic_content').style.display = 'none';
    document.querySelector('div.górny_pasek').style.display = 'none';
    document.querySelector('div.edycja').style.display = 'block';
    document.querySelector('h1#id_edition_header').innerHTML = 'Edycja głosów kandydata: ' + candidates[candidate];
    document.querySelector('input#id_votes').value = og;
    document.querySelector('form#edycja').action = `javascript: editVotes(${wnPk}, ${obwPk}, ${og}, ${wk}, ${wg});`;
}


function editVotes(wnPk, obwPk, og, wk, wg) {
    let csrftoken = getCookie('csrftoken');
    let input = document.querySelector(`input#id_votes`).value;
    let errMsg = document.querySelector('p.error');
    errMsg.innerHTML = '';
    try {
        if (input < 0) {
            throw 'Proszę podać nieujemną liczbę głosów';
        }
        let odds = input - og;
        if (odds + wg > wk) {
            throw 'Co za dużo, to niezdrowo';
        }
        let req = new XMLHttpRequest();
        req.open('POST', `${url}edit_votes${wnPk}`, true);
        let msg = `liczba_głosów=${input}`;
        req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        req.setRequestHeader("Content-lenght", msg.length);
        req.setRequestHeader("X-CSRFToken", csrftoken);
        let errorMsg = '';
        req.onreadystatechange = function () {
            if (req.readyState === XMLHttpRequest.DONE && req.status === 200) {
                try {
                    if (this.responseText !== '') {
                        let errors = JSON.parse(this.responseText);
                        errorMsg = errors['liczba_głosów'][0].message;
                        throw errorMsg;

                    }
                    document.querySelector('div.dynamic_content').style.display = 'block';
                    document.querySelector('div.górny_pasek').style.display = 'block';
                    document.querySelector('div.edycja').style.display = 'none';
                    updateWrapper(`obw${obwPk}`);
                }
                catch (err) {
                    errMsg.innerHTML = err;
                }
            }
        };
        req.send(msg);
    }
    catch (err) {
        errMsg.innerHTML = err;
    }
}



