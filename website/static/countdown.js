countdown();

// use of anonymous function
setInterval(function() {
    countdown();
}, 1000)

function countdown() 
{
    let item = document.getElementById('next')

    const race_date = new Date(item.getAttribute('date'))
    const current_date = new Date()
    
    let timestamp_race = race_date.getTime(); // get ms
    let timestamp_current = current_date.getTime(); // get ms
    
    const seconds = 1000;
    const minutes = 1000 * 60;
    const hours = minutes * 60;
    const days = hours * 24;
    
    
    let timeRemaining = timestamp_race -  timestamp_current;
    
    let d = Math.floor(timeRemaining/days);
    let h = Math.floor(timeRemaining/hours);
    let m = Math.floor(timeRemaining/minutes);
    let s = Math.floor(timeRemaining/seconds);
    
    display_days = d
    display_hours = h - (d * 24) ;
    display_minutes = m - (h * 60);
    display_seconds = s - (m * 60);
    console.log(display_days, display_hours, display_minutes, display_seconds);

    document.getElementById('days').innerHTML = display_days;
    document.getElementById('hours').innerHTML = display_hours;
    document.getElementById('minutes').innerHTML = display_minutes;
    document.getElementById('seconds').innerHTML = display_seconds;
}
