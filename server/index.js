var express = require("express");
var bodyParser = require("body-parser");
var app = express();
var fs = require('fs');
var path = require('path');
var STORAGE_PATH = '/Users/jvanderdoes/Pictures/UXRecorder';

//http://stackoverflow.com/questions/20267939/nodejs-write-base64-image-file
function decodeBase64Image(dataString) {
  var matches = dataString.match(/^data:([A-Za-z-+\/]+);base64,(.+)$/),
    response = {};

  if (matches.length !== 3) {
    return new Error('Invalid input string');
  }

  response.type = matches[1];
  response.data = new Buffer(matches[2], 'base64');

  return response;
}

app.use(bodyParser.json({limit: '100MB'}));

app.post('/save',function(req, res){
  console.log('Logging interaction');
  var imageBuffer = decodeBase64Image(req.body.image),
    timestamp = new Date().getTime(),
    imagePath = path.join(STORAGE_PATH, timestamp+'.jpg'),
    jsonPath = path.join(STORAGE_PATH, timestamp+'.json');

  fs.writeFile( imagePath, imageBuffer.data, function(err) {
    fs.writeFile( jsonPath, JSON.stringify(req.body.data.event, null, 2), function(err) {
      res.send('complete');
    });
  });
});

app.get('/',function(req, res){
  res.send('alive');
});

var server = app.listen(3000, function () {
  var port = server.address().port;
  console.log('Example app listening on port %s', port);
});



