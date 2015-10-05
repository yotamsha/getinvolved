var mongoose = require("mongoose");
var dbConnection = require("../modules/db-connection");

var taskSchema = mongoose.Schema({
    name: String
});

var Task = dbConnection.model('Task', taskSchema);

module.exports = Task;
