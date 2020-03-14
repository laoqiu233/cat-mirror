function createWeatherModule() {
    let config = {
        // Put your Weatherbit.io API key here
        key: "",
        forecast_days: 5
    }

    let module = document.getElementById("module-weather");
    let city;

    fetch("http://ip-api.com/json").then(data => {
        if (data.ok) {
            data.json().then(json => {
                city = json.city;
                updateWeather()
                setInterval(updateWeather, 1000 * 60 * 60) // Update every hour
            })
        } else {
            module.innerHTML = "<h2>Something went wrong with the weather module!</h2>"
        }
    })

    function updateWeather() {
        fetch(`https://api.weatherbit.io/v2.0/current?city=${city}&key=${config.key}`)
        .then(resp => {
            if (!resp.ok) {
                if (resp.status==403) {
                    module.innerHTML = "<h1>Invalid API key!</h1>";
                } else {
                    module.innerHTML = `<h1>Error with stsatus code ${resp.status}</h1>`;
                }
                return;
            }
            resp.json().then(json => {
                module.innerHTML = "";
                let header = document.createElement("header");
                let data = json.data[0];
                let icon = document.createElement("img");
                icon.src = `https://www.weatherbit.io/static/img/icons/${data.weather.icon}.png`;
                icon.style.width = "12rem";
                header.appendChild(icon);
                header.innerHTML += `<h1>${data.temp}°C</h1>`;
                module.appendChild(header);
                module.innerHTML += `<br><h3>Weather Forecast for ${city}</h3>`
                
                fetch(`https://api.weatherbit.io/v2.0/forecast/daily?city=${city}&key=${config.key}`)
                .then(resp => resp.json())
                .then(json => {
                    let table = document.createElement("table");
                    let forecast = json.data;
                    for (let i=1; i<=Math.min(15, config.forecast_days); i++) {
                        let row = document.createElement("tr");
                        let date = new Date(forecast[i].datetime);
                        //console.log(forecast[i]);
                        row.innerHTML = `
                        <td>${date.format(i <= 3 ? "%U" : "%m-%d")}</td>
                        <td><img src="https://www.weatherbit.io/static/img/icons/${forecast[i].weather.icon}.png" style="max-width:5rem"></td>
                        <td>${forecast[i].high_temp}°C</td>
                        <td style="color:#CCC">${forecast[i].low_temp}°C</td>
                        `;
                        table.appendChild(row);
                    }
                    module.appendChild(table);
                });
            })
        })
    }
}

createWeatherModule();