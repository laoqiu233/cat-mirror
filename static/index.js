startJsonSocket(true);
startMessageSocket(true);

modules.forEach((item) => {
    setJsonSocketHandler(item, (data) => {
        Vue.set(app, item, data);
    })
})