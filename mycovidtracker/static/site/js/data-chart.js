var stateName = "";
var today = new Date();
var start_date = getStartDate();
var end_date = getDateString(getEndDate());
var ctx = document.getElementById('data-chart').getContext('2d');

$('#state-select').change(function() {
    stateName = document.getElementById('state-select').value;
    destroyChartIfExists();
    generateChart(stateName, start_date, end_date);
});

$('#start-month').change(function() {
    start_date = getStartDate();
    destroyChartIfExists();
    generateChart(stateName, start_date, end_date);
});

$('#start-day').change(function() {
    start_date = getStartDate();
    destroyChartIfExists();
    generateChart(stateName, start_date, end_date);
});

$('#start-year').change(function() {
    start_date = getStartDate();
    destroyChartIfExists()
    generateChart(stateName, start_date, end_date);
});

$('#prediction-days').change(function() {
    end_date = getDateString(getEndDate());
    console.log(end_date);
    destroyChartIfExists();
    generateChart(stateName, start_date, end_date);
});

$('#trendline-option').change(function() {
    destroyChartIfExists();
    generateChart(stateName, start_date, end_date);
});

function generateChart(stateName, start_date, end_date) {
    chart = new Chart(ctx, {
        type: 'line',
        data: generateStateChartData(stateName, start_date, end_date),
        options: {
            responsive: true,
            layout: {
                padding: {
                    left: 25,
                    right: 25
                },
            },
            scales: {
                xAxes: [{
                    display: true,
                    type: 'time',
                    time: {
                        parser: 'YYYY-MM-DD',
                        tooltipFormat: 'll',
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'Date'
                    }
                }],
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Cases'
                    }
                }]
            }
        }
    });
    console.log(chart.data);
}

function getStartDate() {
    return  document.getElementById('start-year').value +
            "-" +
            document.getElementById('start-month').value +
            "-" +
            document.getElementById('start-day').value;
}

function getDateString(date) {
    var dd = String(date.getDate()).padStart(2,'0');
    var mm = String(date.getMonth() + 1).padStart(2, '0');
    var yyyy = date.getFullYear();
    return yyyy + "-" + mm + "-" + dd;
}

function getEndDate() {
    var endDate = new Date();
    var endDay = endDate.getDate() + parseInt(document.getElementById('prediction-days').value);
    endDate.setDate(endDay);
    return endDate;
}

function destroyChartIfExists() {
    if (typeof chart !== 'undefined') {
        chart.destroy();
    }
}