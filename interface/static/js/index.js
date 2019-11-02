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
        renderPrivs(data);
    });
}

function renderPrivs(data){
    const listEl = document.querySelector('#possible_privs');
    // make sure list is cleared first
    while(listEl.firstChild){
        listEl.removeChild(listEl.firstChild);
    }

    data['context'].forEach((priv) => {
        renderListItem(listEl, priv.priv_name);
    })
};

function renderListItem(listEl, inputString){
    const listItem = document.createElement('li');
    listEl.appendChild(listItem);
    const checkbox = document.createElement('input');
    checkbox.type = "checkbox";
    checkbox.name = inputString;
    listItem.appendChild(checkbox);
    listItem.appendChild(document.createTextNode(inputString));
}

let addPrivFormEl = document.querySelector("#add_priv");
const addPrivHandler = async (e) => {
    e.preventDefault();
    let addPrivForm = new FormData(addPrivFormEl);
    let priv = addPrivForm.get('add_priv');
    data = {add_priv: priv}
    const res = await postData('http://127.0.0.1:8000/interface/possibleprivilege/add', data);
    console.log(res);
    if(res.context.hasOwnProperty('added_priv')){
        const listEl = document.querySelector('#possible_privs');
        renderListItem(listEl, res.context.added_priv);
    }
};
addPrivFormEl.addEventListener("submit", addPrivHandler);

const toggleCheckbox = document.querySelector("#toggle_select_all");
toggleCheckbox.addEventListener("click", (e) =>{
    const checkboxContainer = document.querySelector(".possible_privs_checkboxes");
    const checkboxes = checkboxContainer.querySelectorAll("input[type=checkbox]");
    const srcChecked = e.target.checked;
    checkboxes.forEach((checkbox) => {
        checkbox.checked = srcChecked;
    });
});

const deletePrivFormEl = document.querySelector("#delete_priv");
const deletePrivHandler = async (e) => {
    e.preventDefault();
    const checkboxes = document.querySelector(".possible_privs_checkboxes").querySelectorAll("input[type=checkbox]");
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