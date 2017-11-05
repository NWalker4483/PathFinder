/*
 * A chat server. Client codes can be found in ../resources/chat-client
 * To run server, execute node chat.js
 * To run client, navigate to ../resources/chat-client/client.html from browser
 */
var polyline = require('@mapbox/polyline');


    var http = require('http'),
    fs = require('fs'),
    // NEVER use a Sync function except at start-up!
    index = fs.readFileSync(__dirname + '/index.html');
    // Send index.html to all requests
    var app = http.createServer(function(req, res) {
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.end(index);
    });
    
    // Socket.io server listens to our app
    var io = require('socket.io').listen(app);
    
    // Send current time to all connected clients
    function sendTime() {
    io.emit('time', { time: new Date().toJSON() });
    /*msg=polyline.decode(msg);
    console.log(msg);
    */}
    // Send current time every 10 secs
    setInterval(sendTime, 5000);
    // Emit welcome message on connection
    io.on('connection', function(socket) {
    // Use socket to communicate with this particular client only, sending it it's own id
    socket.emit('welcome', { message: 'Welcome!', id: socket.id });
    
    socket.on('i am client', console.log);
    });
    
    app.listen(3000);