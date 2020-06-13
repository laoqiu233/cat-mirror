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

var json_socket = undefined;
var msg_socket = undefined;

/**
 * Start the json socket
 * @param {Boolean} history 
 */
function startJsonSocket(history=false) {
    json_socket = new EventSource(`/sockets/json?history=${history}`);
}

/**
 * Start the message socket
 * @param {Boolean} history 
 */
function startMessageSocket(history=false) {
    msg_socket = new EventSource(`/sockets/message?history=${history}`);
}

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