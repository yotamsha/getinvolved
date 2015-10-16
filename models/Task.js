var mongoose = require("mongoose");
var dbConnection = require("../modules/db-connection");

var taskSchema = mongoose.Schema({
    name: String,
    createdAt: { type: Date, default: Date.now },
    city: String,
    immediate: Boolean
});

taskSchema.statics.get = function (taskDictionary, cb) {
    var taskQuery = createTaskQuery(taskDictionary);
    Task.find(taskQuery, cb);
};

var Task = dbConnection.model('Task', taskSchema);

function createTaskQuery(taskDictionary) {
    var query = {};
    if (taskDictionary.date) {
        if (taskDictionary.date.from) {
            query.createdAt.$gt = taskDictionary.date.from;
        }
        if (taskDictionary.date.to) {
            query.createdAt.$lt = taskDictionary.date.to;
        }
    }

    if (taskDictionary.city) {
        query.city = taskDictionary.city;
    }

    if (taskDictionary.location) {
        // TODO: Add spatial query - check link
        // https://dzone.com/articles/geospatial-queries-mongoose
    }

    if (taskDictionary.immediate) {
        query.immediate = true;
    }

    if (taskDictionary.tags) {
        // TODO: Find out what tags are
    }

    // I added this for debugging
    if (taskDictionary.name) {
        query.name = taskDictionary.name;
    }

    return query;
}


/*
taskDictionary = {
    date: {
        from: Number,
        to: Number
    },
    city: String,
    location: {
        coords: {
            lat: Number,
            long: Number
        },
        radius: Number (in KM)
    }
    immediate: Boolean,
    tags: [Number]
}
* */

module.exports = Task;
