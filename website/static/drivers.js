let items = document.getElementsByClassName('drivers-card')


for (let i=0; i<items.length; i++) {
    
    items[i].addEventListener('click', () => {
        let driver_id = items[i].getAttribute('driver_id')
        let url = `/driver/${driver_id}`
        window.location.href = url; 
    });
}