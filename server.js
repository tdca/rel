var express = require('express');

var app = express();

app.use(function(req, res, next){
	console.log('[%s] %s %s', req.method, req.url, new Date().toString());
	next();
});

app.use(express.static(__dirname));

app.listen(3000);

