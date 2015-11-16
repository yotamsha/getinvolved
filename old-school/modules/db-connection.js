var mongoose = require('mongoose');
var config = require('../old-school/config');
var mongoDBConnection = mongoose.createConnection(config.mongodb.host, config.mongodb.options);

module.exports = mongoDBConnection;