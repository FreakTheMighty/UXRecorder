var express = require("express");
var bodyParser = require("body-parser");
var app = express();

app.use(bodyParser.json({limit: '100MB'}));

app.post('/save',function(req, res){
	console.log('body', req.body);
	res.send('complete');
});

app.get('/',function(req, res){
	res.send('hello');
});

var server = app.listen(3000, function () {
  var host = server.address().address;
  var port = server.address().port;
  console.log('Example app listening at http://%s:%s', host, port);
});



