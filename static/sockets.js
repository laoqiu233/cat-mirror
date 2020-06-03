var json_socket = new EventSource('/sockets/json');
var msg_socket = new EventSource('/sockets/message')

/**
 * Callback function for json socket handlers
 * @callback jsonCallback
 * @param {Object} obj 
 */

 /**
 * Callback function for message socket handlers
 * @callback msgCallback
 * @param {string} message 
 */

/**
 * Sets handler for incoming JSON messages
 * @param {string} module 
 * @param {jsonCallback} callback 
 */
function setJsonSocketHandler(module, callback) {
    json_socket.addEventListener(module, (e) => callback(JSON.parse(e.data)));
}

/**
 * Sets handler for incoming plain messages
 * @param {string} module 
 * @param {msgCallback} callback 
 */
function setMessageSocketHandler(module, callback) {
    msg_socket.addEventListener(module, (e) => callback(e.data));
}