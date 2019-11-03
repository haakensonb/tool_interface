function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
// console.log(csrftoken);

function getAndRenderPrivs(){
    getData('http://127.0.0.1:8000/interface/all_possible_privs')
    .then(data => {
        renderList(data, "possible_privs", renderPossiblePriv);
    });
}

function getAndRenderRolesAndPrivs(){
    getData('http://127.0.0.1:8000/interface/roles_and_privs')
    .then(data => {
        renderList(data, "roles", renderRoleAndPriv);
    });
}

function clearList(listEl){
    while(listEl.firstChild){
        listEl.removeChild(listEl.firstChild);
    }
}

function renderList(data, listSelector, callback){
    const listEl = document.querySelector(`#${listSelector}`);
    // make sure the list is cleared
    clearList(listEl);

    data['context'].forEach((data) => {
        callback(listEl, data);
    })
};

function renderPossiblePriv(listEl, priv){
    const listItem = document.createElement('li');
    listEl.appendChild(listItem);
    const checkbox = document.createElement('input');
    checkbox.type = "checkbox";
    checkbox.name = priv.priv_name;
    listItem.appendChild(checkbox);
    listItem.appendChild(document.createTextNode(priv.priv_name));
}

function renderRoleAndPriv(listEl, role_and_priv){
    const listItem = document.createElement('li');
    listEl.appendChild(listItem);
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.name = role_and_priv.role_name;
    listItem.appendChild(checkbox);
    listItem.appendChild(document.createTextNode(role_and_priv.role_name));
    // render privs for role
    const privList = document.createElement('ul');
    listItem.appendChild(privList);
    role_and_priv.privs.forEach(priv => {
        const privItem = document.createElement('li');
        privItem.innerText = priv;
        privList.appendChild(privItem)
    });

}


const addPrivFormEl = document.querySelector("#add_priv");
const addPrivHandler = async (e) => {
    e.preventDefault();
    const addPrivForm = new FormData(addPrivFormEl);
    const priv = addPrivForm.get('add_priv');
    data = {add_priv: priv}
    const res = await postData('http://127.0.0.1:8000/interface/possibleprivilege/add', data);
    console.log(res);
    if(res.context.hasOwnProperty('added_priv')){
        const listEl = document.querySelector('#possible_privs');
        renderPossiblePriv(listEl, res.context.added_priv);
    }
};
addPrivFormEl.addEventListener("submit", addPrivHandler);

// could be changed so that one function handles addPrivHandler and addRoleHandler
// but they might end up being different in the future so for now they will get their own functions
const addRoleFormEl = document.querySelector("#add_role");
const addRoleHandler = async (e) => {
    e.preventDefault();
    const addRoleForm = new FormData(addRoleFormEl);
    const role = addRoleForm.get("role");
    data = {role: role};
    const res = await postData('http://127.0.0.1:8000/interface/role/add', data);
    console.log(res);
    if(res.context.hasOwnProperty('role')){
        const listEl = document.querySelector("#roles");
        renderRoleAndPriv(listEl, res.context.role);
    }
};
addRoleFormEl.addEventListener("submit", addRoleHandler);

function toggleAllCheckboxHandler(e, checkboxSelector){
    const checkboxContainer = document.querySelector(`#${checkboxSelector}`);
    const checkboxes = checkboxContainer.querySelectorAll("input[type=checkbox]");
    const srcChecked = e.target.checked;
    checkboxes.forEach((checkbox) => {
        checkbox.checked = srcChecked;
    });
}

const togglePossiblePrivCheckbox = document.querySelector("#toggle_possible_priv_select");
togglePossiblePrivCheckbox.addEventListener("click", (e) => toggleAllCheckboxHandler(e, "possible_privs_checkboxes"));

const toggleRolesCheckbox = document.querySelector("#toggle_role_select");
toggleRolesCheckbox.addEventListener("click", (e) => toggleAllCheckboxHandler(e, "roles_checkboxes"));

const deletePrivFormEl = document.querySelector("#delete_priv");
const deletePrivHandler = async (e) => {
    e.preventDefault();
    const checkboxes = document.querySelector("#possible_privs_checkboxes").querySelectorAll("input[type=checkbox]");
    privsToDel = [];
    checkboxes.forEach((checkbox) => {
        if(checkbox.checked){
            privsToDel.push(checkbox.name);
        }
    });
    data = {delete_privs: privsToDel};
    await postData('http://127.0.0.1:8000/interface/possibleprivilege/delete', data);
    getAndRenderPrivs();

};
deletePrivFormEl.addEventListener("submit", deletePrivHandler);

// could maybe be merged with deletePrivFormEl
const deleteRoleFormEl = document.querySelector("#delete_role");
const deleteRoleHandler = async (e) => {
    e.preventDefault();
    const checkboxes = document.querySelector("#roles_checkboxes").querySelectorAll("input[type=checkbox]");
    rolesToDel = [];
    checkboxes.forEach((checkbox) => {
        if(checkbox.checked){
            rolesToDel.push(checkbox.name);
        }
    });
    data = {roles: rolesToDel};
    await postData('http://127.0.0.1:8000/interface/role/delete', data);
    getAndRenderRolesAndPrivs();
}
deleteRoleFormEl.addEventListener("submit", deleteRoleHandler);

async function postData(url, data){
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(data)
    });
    return await response.json();
}

async function getData(url){
    const response = await fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });
    return response.json();
}

getAndRenderPrivs();
getAndRenderRolesAndPrivs();