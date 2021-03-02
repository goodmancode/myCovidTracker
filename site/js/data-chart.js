var ctx = document.getElementById('data-chart').getContext('2d');
var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'line',

    // The data for our dataset
    data: {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
        datasets: [{
            label: '# Cases',
            backgroundColor: 'rgba(255,0,0,0.25)',
            borderColor: 'red',
            data: [0, 10, 5, 2, 20, 30, 45]
        }]
    },

    // Configuration options go here
    options: {
        title: {
            display: false,
            text: 'COVID Cases',
            fontSize: 36
        },
        layout: {
            padding: {
                left: 25,
                right: 25
            }
        }
    }
});