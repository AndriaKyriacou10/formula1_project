let items = document.getElementsByClassName('constructors-card')


for (let i=0; i<items.length; i++) {
    
    items[i].addEventListener('click', () => {
        let constructor_id = items[i].getAttribute('constructor_id')
        let url = `/team/${constructor_id}`
        window.location.href = url; 
    });
}