function createHeadlinesModule() {
    let config;
    let news;
    let module = document.getElementById('module-headlines');

    function getNews(render) {
        fetch(`https://newsapi.org/v2/top-headlines?apiKey=${config.key}&country=${config.country}`)
        .then(data => {
            if (!data.ok) {
                module.innerHTML = '<h2>Something went wrong!</h2>';
                if (data.status=401) {
                    module.innerHTML = '<h2>Invalid API key</h2>';
                }
                return;
            }
            data.json().then(json => {
                news = json.articles;
                fetch("/headlines/news", {
                    method: "POST",
                    body: JSON.stringify(news),
                    headers: {
                        'content-type': 'application/json'
                    },
                    credentials: "include"
                })
                if (render) {
                    renderHeadline(0);
                }
            })
        })
    }

    function renderHeadline(index) {
        if (news.length == 0) {
            module.innerHTML = "<h3>There are no news articles at this moment.</h3>";
        } else {
            let split_index = news[index].title.split('').reverse().indexOf('-');

            module.innerHTML = `
                <h3 style='font-size:2.5rem;'>${news[index].title.slice(0, news[index].title.length - 1 - split_index).trim()}</h3>
                <h4 style='color:#AAA;font-size:2rem;'>${news[index].title.slice(news[index].title.length - split_index).trim()} - ${new Date(news[index].publishedAt).format("%Y-%m-%d %H:%M:%S")}</h4>
            `;

            console.log(news[index].title);
        }

        module.style.opacity = 1;
        
        module.addEventListener('transitionend', () => {
            setTimeout(() => {
                module.style.opacity = 0;
                module.addEventListener('transitionend', () => {
                    renderHeadline(index + 1 >= news.length ? 0 : index+1);
                }, {once: true})
            }, 10000)
        }, {once: true})
    }

    // Get API key and region
    fetch('/headlines/config', {credentials: 'include'})
    .then(data => data.json())
    .then(json => {
        config = json;
        getNews(true);
        setInterval(() => getNews(false), 5 * 60 * 1000) // Get new news every five minutes
    })
}

createHeadlinesModule();