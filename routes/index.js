var express = require('express');
var router = express.Router();
var fs = require('fs')
var mongodb = require('mongodb');
var url = require('url');

/*var connectionUri = url.parse(process.env['MONGOHQ_URL']);
var dbName = connectionUri.pathname.replace(/^\//, '');*/

/* GET home page. */
router.get('/', function(req, res) {
  	var carriers = ["Select Carrier", "AT&T", "Verizon", "Sprint", "T-Mobile", "MetroPCS", "Other"];
  	var regionArea = {};
  	var regionList = Array();
  	fs.readFile('./public/Data/msw_dict.txt', 'utf-8', function(err, spotDict) {
		if (err) {return console.error(err);}
		data = JSON.parse(spotDict);
		for (var region in data) {
			if (data.hasOwnProperty(region)) {
				regionList.push(region);
				var inner = Array();
				for (var area in data[region]) {
					if (data[region].hasOwnProperty(area)) {
						inner.push(area);
					}
				}
				regionArea[region] = inner;
			}
		}
		res.render('index', {map: regionArea, regions: regionList, car: carriers});
		res.write(JSON.stringify(regionArea));
		res.end();
		//res.end(spotDict["North America"]["California, Central"]["Central California"][0]);
	});
});

router.get('/spots-in-area', function(req, res) {
	fs.readFile('./public/Data/msw_dict.txt', 'utf-8', function(err, spotDict) {
		if (err) {return console.error(err);}
		var data = JSON.parse(spotDict);
		var replyHTML = '<select class="spots"><option value="null">Select Spot</option>'
		var locatedData = data[req.param('reg')][req.param('ar')];
		var counties = Array();
		for (var location in locatedData) {
			if (locatedData.hasOwnProperty(location)) {
				counties.push(location);
				replyHTML += '<optgroup label="' + location + '">';
				for (var i = 0; i < locatedData[location].length; i++) {
					replyHTML += '<option value="' + locatedData[location][i] + '">' + locatedData[location][i] + '</option>';
				}
				replyHTML += '</optgroup>'
			}
		}
		replyHTML += '</select>';
		res.end(replyHTML);
	});
});

router.post('/add-spot', function(req, res) {
	
	var phoneNumber = req.param('phoneNumber');
	var cellCarrier = req.param('cellCarrier');
	var location = req.param('location');
	mongodb.Db.connect(process.env.MONGOHQ_URL, function(err, db) {
		if (err) {return console.error(err);}
		var collection = new mongodb.Collection(db, 'surf-notification-users');
		var user = collection.find({phone_number: phoneNumber});
		user.toArray(function(err, userEntryList) {
			if (err) {return console.error(err);}
			if (userEntryList.length > 0) {
				var record = userEntryList[0];
				//console.log(JSON.stringify(record));
				var places = record['spots'];
				/*if (places.length == 1) {
					var temp = places;
					var places = new Array();
					places.push(temp);
				}*/
				//console.log(places.length);
				console.log('location: ' + location);
				console.log('places: ' + String(places));
				if (! (location in places)) {
					console.log('here');
					places.push(location);
				}
				collection.update({phone_number: phoneNumber}, {$set: {spots: places}}, function(err, result) {
					if (err) {return console.error(err);}
				});
			} else {
				var a = Array();
				a.push(location);
				collection.insert({phone_number: phoneNumber, cell_carrier: cellCarrier, spots: a}, function(err, result) {
					if (err) {return console.error(err);}
				});
			}
		});
	});
});

router.get('/try-json-msw-data', function(req, res) {
	fs.readFile('./public/Data/msw_dict.txt', 'utf-8', function(err, spotDict) {
		if (err) {return console.error(err);}
		data = JSON.parse(spotDict);
		for (var key in data) {
			if (data.hasOwnProperty(key)) {
				res.write(key + "\n");
			}
		}
		res.end();
		//res.end(spotDict["North America"]["California, Central"]["Central California"][0]);
	});
});

module.exports = router;
