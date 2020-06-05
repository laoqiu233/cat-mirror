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