let elements = document.querySelectorAll('.col-name');

const drivers = [];
elements.forEach((element) => {
    let driver = element.getAttribute('driver-data');
    let driver_json = JSON.parse(driver);
    drivers.push(driver_json);
    
    let header = element.querySelector('#driver-name');
    if (driver_json.number == null) {
        header.classList.add('driver-no-number');
    }
    else {
        header.classList.add('driver-name-compare');
    }
});

if (window.innerWidth <= 770) {
    
    dataHeaders = document.querySelectorAll('.data-headers .data-p')
    dataHeaders.forEach(data => {
        let p = data;
        if (p.textContent.trim() === 'grand prix entries'){
            p.classList.add('data-headers-p')
        }
    });
}

if (window.innerWidth <= 570) {
    
    dataHeaders = document.querySelectorAll('.data-headers .data-p');
    dataHeaders.forEach(data => {
        let p = data;
        if (p.textContent.trim() === 'debut race'){
            p.classList.add('data-headers-debut')
        }
    });
    if (drivers[0].teams.length <=2 && drivers[1].teams.length <= 2){
        table = document.querySelectorAll('.add-border');
        table.forEach(data => {
            data.style.height = '250px';
        });
        tableR = document.querySelectorAll('.add-border table');
        tableR.forEach(data => {
            data.style.height = '250px';
        });
    }
    
}
if (window.innerWidth <= 485) {
    let tr = document.querySelectorAll('tr');
    tr.forEach(data => {
        data.style.height = '60px';
    })
}
if (window.innerWidth <= 340) {
    
    dataHeaders = document.querySelectorAll('.data-headers .data-p')
    dataHeaders.forEach(data => {
        let p = data;
        if (p.textContent.trim() === 'pole positions'){
            p.classList.add('data-headers-pole')
        }
    });

    bestChamp = document.querySelectorAll('.best-pos .data-best')
    bestChamp.forEach(data => {
        let p = data;
        if (p.textContent.trim() === 'best position'){
            p.classList.add('data-headers-pole')
        }
    });
}


let years_col = document.querySelectorAll('.years-col');
let best_pos = document.querySelectorAll('.best-pos');

drivers.forEach((driver,index) => {
    let champ_years = driver.champs.years.split(' ');

    if (champ_years.length == 1){
        // if (index == 0)
        //     years_col[index].children[0].classList.add('best-p-1');
    }
    if (champ_years.length > 4){
        years_col[index].children[0].classList.add('years-max-w');
        if (index ==  0){
            years_col[index].children[0].style.marginLeft = '5%';
        }
        else
            years_col[index].children[0].style.marginLeft = '28%';
            // years_col[index].children[0].style.marginLeft = '0%';

        if (window.innerWidth <= 992 && index == 1)
            years_col[index].children[0].style.marginLeft = '35%';
        
        if (window.innerWidth <= 991){
            if (index == 0)
                best_pos[index].children[0].style.marginRight = '25%';
            else
                years_col[index].children[0].style.marginLeft = '32%';  
        }
        if (window.innerWidth <= 767 && index == 1)
            years_col[index].children[0].style.marginLeft = '36%';
        
        if (window.innerWidth <= 435){
            if (index == 0)
                years_col[index].children[0].style.marginLeft = '12%';
        }
        if (window.innerWidth <= 375 && index == 1)
            years_col[index].children[0].style.marginLeft = '38%';
    }
    else {
        if (window.innerWidth <= 991 && champ_years.length == 3) {
            years_col[index].children[0].classList.add('best-p-width');
            if (index == 0) {
                years_col[index].children[0].classList.add('best-p-width-1');
                best_pos[index].children[0].style.marginRight = '33%';
            }
            else{
                years_col[index].children[0].style.marginLeft = '34%';
            }
        }
        if (window.innerWidth <= 767 && champ_years.length == 3) {
            if (index == 0)
                years_col[index].children[0].style.marginRight = '39%';
            else
                years_col[index].children[0].style.marginLeft = '25%';
        }
        if (window.innerWidth <= 470) {
            years_col[index].children[0].classList.add('best-p-width');
            if (index == 0){
                years_col[index].children[0].style.marginLeft = '18%';
            }
            else{
                years_col[index].children[0].style.marginLeft = '40%';
            }
                
        }
        if (window.innerWidth <= 435) {
            if (champ_years.length == 1){
                if (index == 0)
                    years_col[index].children[0].style.marginLeft = '16%';
                else
                    years_col[index].children[0].style.marginLeft = '39%';
            }
            else {
                if (index == 0){
                    years_col[index].children[0].style.marginLeft = '10%';
                }
                else {
                    years_col[index].children[0].style.marginLeft = '38%';
                }
            }
        }
        if (window.innerWidth <= 410) {
            if (index == 0){

            }
            else {
                best_pos[index].children[0].style.marginLeft = '22%';
            }
        }
        if (window.innerWidth <= 375) {
            if (index == 0){
                years_col[index].children[0].style.marginLeft = '17%';
                best_pos[index].children[0].style.marginRight = '22%';
            }
            else {
                years_col[index].children[0].style.marginLeft = '32%';
            }
            if (champ_years.length == 1){
                if (index == 0)
                    years_col[index].children[0].style.marginLeft = '18%';
                else
                    years_col[index].children[0].style.marginLeft = '35%';
            }
        }
        if (window.innerWidth <= 320) {
            if (index == 0){
                years_col[index].children[0].style.marginRight = '35%';
                best_pos[index].children[0].style.marginRight = '23%';
            }
            else{
                years_col[index].children[0].style.marginLeft = '30%';
                best_pos[index].children[0].style.marginLeft = '23%';
                if (index == 1 && champ_years.length == 1)
                    years_col[index].children[0].style.marginLeft = '30%';
            }
        }
    }
});



const driver_ids = [drivers[0].id, drivers[1].id];
const params = {
    'id1': drivers[0].id,
    'id2': drivers[1].id
};

pointsPlot()

if (parseFloat(drivers[0].win_ratio) > 0 || parseFloat(drivers[1].win_ratio) > 0)
{
    winRatio()
}

if(parseFloat(drivers[0].podium_ratio) > 0 || parseFloat(drivers[1].podium_ratio) > 0)
{
    podiumRatio()
}

async function pointsPlot() {
    let response = await fetch('/compare/plots?' + new URLSearchParams(params).toString());
    let data = await response.json();
    
    // x and y data for plot
    x1 = data.seasons[0];
    x2 = data.seasons[1];

    y1 = data.points[0];
    y2 = data.points[1];


    const indexes1 = [];
    const indexes2 = [];
    for (let i=0; i<x1.length - 1; i++){
        if(x1[i+1] - x1[i] != 1){
            indexes1.push(i);
        }
    }
    for (let i=0; i<x2.length - 1; i++){
        if(x2[i+1] - x2[i] != 1){
            indexes2.push(i);
        }
    }
    
    var plot_1 = {
        x: '',
        y: '',
        xaxis: 'x1',
        yaxis: 'y1',
        mode: 'lines+markers',
        name: drivers[0].name,
        line: {
            dash: 'dot',
            color: '#00ffee',
            width: 4
        },
        marker: {
            color: '#00635d',
            size: 6
        },
        showlegend: false
    };

    var plot_2 = {
        x: '',
        y: '',
        xaxis: 'x2',
        yaxis: 'y2',
        mode: 'lines+markers',
        name: drivers[1].name,
        line: {
            dash: 'dot',
            color: '#d900d9',
            width: 4
        },
        marker: {
            color: '#730073',
            size: 6
        },
        showlegend: false
    };

    var plots = [];

    if (indexes1.length == 0) {
        let plot_temp = {...plot_1};
        plot_temp.x = x1;
        plot_temp.y = y1;
        plots.push(plot_temp);
    }
    else {
        splitData(indexes1, plot_1, x1, y1, plots);
    }
    if (indexes2.length == 0) {
        let plot_temp;
        plot_temp = {...plot_2};
        plot_temp.x = x2;
        plot_temp.y = y2;
        plots.push(plot_temp);
    }
    else {
        splitData(indexes2, plot_2, x2, y2, plots);
    }

    const fonts = { family: 'Roboto Slab', size: 28 ,color: '#fff' };
    const xlabel = 'Seasons';
    const ylabel = 'Points';
    var layout = {
        height:600,
        grid: {rows: 2, columns: 1, pattern: 'independent'},
        paper_bgcolor: '#000',
        plot_bgcolor: '#000',
        font: {
            color: '#fff'
        },
        xaxis: {
            title: xlabel,
            tickvals: x1,
            ticktext: x1,
            linecolor: '#a1a1a1',
            gridcolor: '#3c3c3d'
        },
        xaxis2: {
            title: xlabel,
            tickvals: x2,
            ticktext: x2,
            linecolor: '#a1a1a1',
            gridcolor: '#3c3c3d'
        },
        yaxis: {
            title: ylabel,
            range: [0, Math.max(...y1)+100],
            domain: [0.6, 1],
            linecolor: '#a1a1a1',
            gridcolor: '#3c3c3d',
            linewidth: 2
        },
        yaxis2: {
            title: ylabel,
            range: [0, Math.max(...y2)+100] ,
            domain: [0, 0.4],
            linecolor: '#a1a1a1',
            gridcolor: '#3c3c3d',
            linewidth: 2
        },
        margin: {
            t: 60,  
            b: 80,  
            // l: 80,  
            // r: 80  
        },
        annotations: [
            {
                x: 0.5,
                y: 1.08,
                xref: 'paper',
                yref: 'paper',
                text: drivers[0].name,
                showarrow: false,
                font: fonts,
                align: 'center'
            },
            {
                x: 0.5,
                y: 0.43,
                xref: 'paper',
                yref: 'paper',
                text: drivers[1].name,
                showarrow: false,
                font: fonts,
                align: 'center'
            }
        ],

    };
    var config = {
        responsive: true, 
        modeBarButtonsToRemove:[],
        toImageButtonOptions: {
            width: 1100,
            height: 900,
            
        }
    };

    if (window.innerWidth <= 770) {
        layout.annotations[1].y = 0.43;
        fonts.size = 14;
        (layout.annotations).forEach(annotation => {
            annotation.font = fonts;
        });
    }
    if (window.innerWidth <= 525) {
        layout.xaxis.tickvals = []
        layout.xaxis.ticktext = []
        layout.xaxis2.tickvals = []
        layout.xaxis2.ticktext = []
        config.modeBarButtonsToRemove = ['zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d', 'hoverClosestCartesian', 'hoverCompareCartesian'];
    }

    Plotly.newPlot('points', plots, layout, config);
    
}

function splitData(indexes,plot,x,y, plots) {
    for(let i=0; i< indexes.length; i++){
        let plot_temp;
        
        if (indexes.length == 1) {
            let start1 = 0;
            let end1 = indexes[i] + 1;
            let start2 = end1;
            let end2 = x.length + 1;
            plot_temp = {...plot};
            plot_temp.x = x.slice(start1,end1);
            plot_temp.y = y.slice(start1,end1);
            plots.push(plot_temp);

            plot_temp = {...plot};
            plot_temp.x = x.slice(start2,end2);
            plot_temp.y = y.slice(start2,end2);
            plots.push(plot_temp);

            break;
        }
        if ( i == 0 ){
            let start1 = 0;
            let end1 = indexes[i] + 1;
            let start2 = end1;
            let end2 = indexes[i+1] + 1;

            plot_temp = {...plot};
            plot_temp.x = x.slice(start1,end1);
            plot_temp.y = y.slice(start1,end1);
            plots.push(plot_temp);

            plot_temp = {...plot};
            plot_temp.x = x.slice(start2,end2);
            plot_temp.y = y.slice(start2,end2);

            plots.push(plot_temp);

        }
        else if( i == indexes.length -1){
            let start = indexes[i]+1;
            let end = x.length + 1;

            plot_temp = {...plot};
            plot_temp.x = x.slice(start,end);
            plot_temp.y = y.slice(start,end);
            
            plots.push(plot_temp);
        }
        else {
            let start = indexes[i]+1;
            let end = indexes[i+1]+1;

            plot_temp = {...plot};
            plot_temp.x = x.slice(start,end);
            plot_temp.y = y.slice(start,end);

            plots.push(plot_temp);
        }
    }
}

function winRatio() {
    var yValue = [parseFloat(drivers[0].win_ratio), parseFloat(drivers[1].win_ratio)];
    var trace1 = {
        x: [drivers[0].name, drivers[1].name],
        y: yValue,
        text: yValue.map(value => value.toFixed(2) + ' %'),
        textposition: 'auto',
        marker: {
            color: ['#00c4b7','#8a008a']
        },
        width: [0.4, 0.4],
        textfont: {
            size: 18,
            color: '#fff'
        },
        type: 'bar',
    };

    var data = [trace1];

    var layout = {
        paper_bgcolor: '#000',
        plot_bgcolor: '#000',

        font: {
            color: '#fff',
        },


        title: {
            text:'Win Ratio',
            font:{
                size: 24
            }
        },
        
        xaxis: {
            title: 'Drivers',
            linecolor: '#a1a1a1',
            size: 16,
            linewidth:2,
        },
        yaxis: {
            range: [0, Math.max(...yValue)+20] ,
            title: 'Win Ratio',
            linecolor: '#a1a1a1',
            size: 16,
            linewidth:2,
            gridcolor: '#3c3c3d',
        }
    };

    var config = {responsive: true, modeBarButtonsToRemove:[]};


    if (window.innerWidth <= 767) {
        trace1.textfont.size = 14;
        layout.xaxis.showticklabels= false;
        data = [trace1];
    }
    if (window.innerWidth <= 525) {
        config.modeBarButtonsToRemove = ['zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d', 'hoverClosestCartesian', 'hoverCompareCartesian'];
    }

    Plotly.newPlot('win-ratio', data, layout, config);

    
}

function podiumRatio() {
    var yValue = [parseFloat(drivers[0].podium_ratio), parseFloat(drivers[1].podium_ratio)];
    var trace1 = {
        x: [drivers[0].name, drivers[1].name],
        y: yValue,
        text: yValue.map(value => value.toFixed(2) + ' %'),
        textposition: 'auto',
        marker: {
            color: ['#00c4b7','#8a008a']
        },
        width: [0.4, 0.4],
        textfont: {
            size: 18,
            color: '#fff'
        },
        type: 'bar',
    };

    var data = [trace1];

    var layout = {
        paper_bgcolor: '#000',
        plot_bgcolor: '#000',

        font: {
            color: '#fff',
        },


        title: {
            text:'Podium Ratio',
            font:{
                size: 24
            }
        },
        
        xaxis: {
            title: 'Drivers',
            linecolor: '#a1a1a1',
            size: 16,
            linewidth:2,
            
        },
        yaxis: {
            range: [0, Math.max(...yValue)+20] ,
            title: 'Podium Ratio',
            linecolor: '#a1a1a1',
            size: 16,
            linewidth:2,
            gridcolor: '#3c3c3d',
        }
    };

    var config = {responsive: true, modeBarButtonsToRemove:[]};

    if (window.innerWidth <= 767) {
        trace1.textfont.size = 14;
        layout.xaxis.showticklabels= false;
        data = [trace1];
    }
    if (window.innerWidth <= 525) {
        config.modeBarButtonsToRemove = ['zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d', 'hoverClosestCartesian', 'hoverCompareCartesian'];
    }

    Plotly.newPlot('podium-ratio', data, layout, config);

    
}




