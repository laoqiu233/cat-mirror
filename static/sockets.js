function setJsonSocketHandler(module, handler) {
    let evt = new EventSource(`/sockets/${module}/json`);
    evt.onmessage = (e) => {
        handler(JSON.parse(e.data));
    }
}

function setMessageSocketHandler(module, handler) {
    let evt = new EventSource(`/sockets/${module}/message`);
    evt.onmessage = (e) => {
        handler(e.data);
    }
}