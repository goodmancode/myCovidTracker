var forecastData = setForecastData();
var historicalCovidData;

function getForecastData() {
    return new Promise(function (resolve, reject) {
        var gsRef = storage.ref('forecast_data.json');
        gsRef.getDownloadURL()
            .then((url) => {
                console.log(url);
                var xhr = new XMLHttpRequest();
                xhr.responseType = 'json';
                xhr.open('GET', url, true);
                xhr.onload = function () {
                    var status = xhr.status;
                    if (status == 200) {
                        var data = xhr.response;
                        console.log(data);
                        resolve(data);
                    }
                    else {
                        reject(status);
                    }
                };
                xhr.send();
            })
            .catch((error) => {
                switch (error.code) {
                    case 'storage/object-not-found':
                      // File doesn't exist
                      console.error("[Firebase Storage] - file not found");
                      break;
                    case 'storage/unauthorized':
                      // User doesn't have permission to access the object
                      console.error("[Firebase Storage] - download not authorized");
                      break;
                    case 'storage/canceled':
                      // User canceled the upload
                      console.error("[Firebase Storage] = download canceled");
                      break;
                    case 'storage/unknown':
                      // Unknown error occurred, inspect the server response
                      console.error("[Firebase Storage] - unknown error");
                      break;
                }
            });
    });
}

$.ajax({
    url: "https://data.cdc.gov/resource/9mfq-cb36.json",
    type: "GET",
    dataType: "json",
    data: {
        "$select" : "submission_date, state, tot_cases",
        "$limit" : 20000,
        "$order" : "submission_date DESC"
    },
    success: function(data) {
        setHistoricalData(data);
    }
});

// Functions that set data once async calls finish
async function setHistoricalData(data) {
    historicalCovidData = await data;
}

async function setForecastData() {
    var data = await getForecastData();
    console.log(data);
    forecastData = data;
}

// Use this function to grab chart data
function generateStateChartData(state, start_date, end_date) {
    var chartData = {
        datasets: [
            {
                label: 'Total Cases',
                backgroundColor: 'rgba(255,0,0,0.25)',
                borderColor: 'red',
                data: getStateSpecificHistorical(state, historicalCovidData, start_date, end_date),
            },
            {
                label: 'Forecasted',
                backgroundColor: 'rgba(0,0,255,0.25)',
                borderColor: 'blue',
                data: getStateSpecificForecast(state, forecastData, start_date, end_date),
            },
        ]
    }
    return chartData;
}

function getStateSpecificHistorical(stateName, historical_data, start_date, end_date) {
        var startInt = dateToInteger(start_date);
        var endInt = dateToInteger(end_date);
        var filtered = historical_data.filter(function(datapoint) {
            submissionDate = dateToInteger(datapoint.submission_date);
            return  stateCodeToFullName(datapoint.state) === stateName &&
                    submissionDate >= startInt &&
                    submissionDate <= endInt;
        });
        var refactored = [];
        for (i = 0; i < filtered.length; i++) {
            var datapoint = {
                x: dateTimeTrimmed(filtered[i].submission_date),
                y: parseInt(filtered[i].tot_cases),
            }
            refactored.push(datapoint);
        }
        return refactored;
}

function getStateSpecificForecast(stateName, forecast_data, start_date, end_date) {
        var startInt = dateToInteger(start_date);
        var endInt = dateToInteger(end_date);
        var filterState = forecast_data.filter(function(stateObject) {
            return  stateObject.state === stateName;
        });
        var stateData = filterState[0].data;
        var filterDates = stateData.filter(function(datapoint) {
            submissionDate = dateToInteger(datapoint.date);
            return  submissionDate >= startInt &&
                    submissionDate <= endInt;
        });
        var refactored = [];
        for (i = 0; i < filterDates.length; i++) {
            var datapoint = {
                x: dateTimeTrimmed(filterDates[i].date),
                y: Math.round(filterDates[i].value),
            }
            refactored.push(datapoint);
        }
        return refactored;
}

function dateTimeTrimmed(date) {
        return date.slice(0,10);
}

function dateToInteger(date) {
        trimTime = dateTimeTrimmed(date);
        removeHyphens = trimTime.replace(/-/g, '');
        return parseInt(removeHyphens);
}
