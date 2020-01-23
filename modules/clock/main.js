function create_clock() {
    Date.prototype.format = function(fmt) {
        var days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
        var o = {
            "%%" : "%",
            "%Y" : this.getFullYear(),
            "%y" : this.getFullYear() % 100,
            "%m" : String(this.getMonth()+1).padStart(2, '0'), 
            "%d" : this.getDate(), 
            "%U" : days[this.getDay()-1],
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

    var module = document.getElementById("module-clock");
    var clock_header = document.createElement("h1");
    var clock_subtitle = document.createElement("h2");
    clock_header.id = "module-clock-time";

    module.appendChild(clock_header);
    module.appendChild(clock_subtitle);

    var format_header, format_subtitle;

    fetch("/clock/format").then(resp => {
        return resp.json()
    }).then(data => {
        format_header = data.header;
        format_subtitle = data.subtitle;

        function update() {
            let time = new Date();
            clock_header.innerHTML = time.format(format_header);
            clock_subtitle.innerHTML = time.format(format_subtitle);
        }
        update();
        setInterval(update, 1000);
    })

    var event_source = new EventSource("/clock/stream");
    event_source.onmessage = e => {
        let format = JSON.parse(e.data);
        console.log(format);
        format_header = format.header;
        format_subtitle = format.subtitle;
    }
}

create_clock();