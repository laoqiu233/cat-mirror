modules.forEach((item) => {
    let evt = new EventSource(`/sockets/${item}/json`);
    evt.onmessage = (e) => {
        Vue.set(app, item, JSON.parse(e.data));
    }
})