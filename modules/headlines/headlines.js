document.getElementById('module-headlines').style.opacity = 1;

setTimeout(headlinesAnimation, 500);

function headlinesAnimation() {
    let duration = 10000;

    setTimeout(() => {
        document.getElementById('module-headlines').style.opacity = 0;
        setTimeout(() => {
            if (app.headlines.n + 1 >= app.headlines.articles.length) app.headlines.n = 0;
            else app.headlines.n++;
            document.getElementById('module-headlines').style.opacity = 1;
            setTimeout(headlinesAnimation, 500);
        }, 500);
    }, duration);
}

let headlines_description_dom = document.createElement('div');
headlines_description_dom.id = 'module-headlines-news-description';
document.getElementById('app').appendChild(headlines_description_dom);

setMessageSocketHandler('headlines', function(msg) {
    if (msg == 'show news') {
        headlines_description_dom.innerHTML = `
        <div class="wrapper">
            <h3>${app.headlines.articles[app.headlines.n].title}</h3>
            <p>${app.headlines.articles[app.headlines.n].description}</p>
            <p style="color:#AAA">Check the full article on the config page!</p>
        </div>
        `
        headlines_description_dom.style.width = '500px';
    } else if (msg == 'hide news') {
        headlines_description_dom.style.width = '0';
    }
});