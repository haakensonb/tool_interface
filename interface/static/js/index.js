fetch('http://127.0.0.1:8000/interface/all_possible_privs')
.then((res) => {
    return res.json();
})
.then((data) => {
    console.log(data);
    create_privs(data)
})

function create_privs(data){
    const listEl = document.querySelector('#possible_privs');
    let listItems = '';
    data['context'].map((priv) => {
        listItems += `
        <li>
            <p>
                ${priv.priv_name} 
            </p>
        </li>
        `;
    })
    listEl.innerHTML = listItems;
};