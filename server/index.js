var express = require("express");
var bodyParser = require("body-parser");
var app = express();

app.use(bodyParser.urlencoded({ extended: false }));

app.post('/save',function(req, res){
  var image = req.body.image;
  var data = req.body.data;
	console.log('image', image);
	console.log('data', data);
});

app.get('/',function(req, res){
	res.send('hello');
});

var server = app.listen(3000, function () {
  var host = server.address().address;
  var port = server.address().port;
  console.log('Example app listening at http://%s:%s', host, port);
});



