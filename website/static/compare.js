let d1_input = document.querySelector("#d1")
let d2_input = document.querySelector("#d2")

d1_input.addEventListener('input', () => search(d1_input, '1'))
d2_input.addEventListener('input', () => search(d2_input, '2'))

async function search(driver_input, number) {
    let row_button = document.querySelector("#row-btn")
    
    let dropdown = document.querySelector('#dropdown-'+number);
    dropdown.style.display = 'block';
    let response = await fetch('/compare/search?q=' + driver_input.value)
    let drivers = await response.json();
    let ul = document.querySelector('#dropdown-list-'+number);
    ul.innerHTML = '';

    if (drivers.length == 0){
        row_button.classList.remove('row-button-toggle'); 
    }
    else {
        row_button.classList.add('row-button-toggle');
    }
    
    for (let i in drivers) {
        let name = drivers[i].name
        let button = document.createElement('button')
        button.type = "button";
        button.className = "list-group-item text-start fs-6";
        
        button.textContent = name;
        ul.appendChild(button);

        button.addEventListener('click', function(){
            driver_input.value = button.textContent;
            ul.innerHTML = '';
            row_button.classList.remove('row-button-toggle');
        });

        window.addEventListener('click', function(){
            row_button.classList.remove('row-button-toggle')
            let dropdown = document.querySelector('#dropdown-'+number);
            dropdown.style.display = 'none';
        });
    }
}


