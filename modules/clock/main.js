function create_clock() {
    Date.prototype.format = function(fmt) {
        var o = {
            "%%" : "%",
            "%Y" : this.getFullYear(),
            "%y" : this.getFullYear() % 100,
            "%m" : String(this.getMonth()+1).padStart(2, '0'), 
            "%d" : this.getDate(), 
            "%H" : String(this.getHours()).padStart(2, '0'),
            "%I" : String(this.getHours() < 13 ? this.getHours() : this.getHours() - 12).padStart(2, '0'),
            "%M" : String(this.getMinutes()).padStart(2, '0'), 
            "%S" : String(this.getSeconds()).padStart(2, '0'),
            "%\\n" : "<br/>"
        };

        for (pattern in o) {
            fmt = fmt.replace(pattern, o[pattern]);
        }

        return fmt;
    }

    var container = document.getElementById("module-clock");
    var clock = document.createElement("h1");
    clock.id = "module-clock-time";

    container.appendChild(clock);

    var format;

    fetch("/clock/format").then(resp => {
        return resp.json()
    }).then(data => {
        format = data.format;

        function update() {
            let time = new Date();
            clock.innerHTML = time.format(format);
        }
        update();
        setInterval(update, 1000);
    })

    var event_source = new EventSource("/clock/stream");
    event_source.onmessage = e => {
        format = e.data;
    }
}

create_clock();