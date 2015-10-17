/**
 * Created by Bar Wachtel on 16/10/2015.
 */
var Task = require('../models/Task');

exports.getTasks = function (req, res, next) {
    var taskDictionary = req.query.taskDictionary ? JSON.parse(req.query.taskDictionary) : {};
    Task.get(taskDictionary, function (err, tasks) {
        if (err) {
            next(err);
        } else {
            if (tasks) {
                res.json({
                    success: true,
                    tasks: tasks
                });
            }
        }
    });
};

exports.createTask = function (req, res, next) {
    var keys = Object.keys(req.body);
    var taskFields = {};

    for (var i = 0; i < keys.length; i++) {
        taskFields[keys[i]] = req.body[keys[i]];
    }

    //var taskFields = JSON.parse(req.query.task);
    Task.create(taskFields, function(err, task) {
        if (err) {
            next(err);
        } else {
            res.json({
                success: true,
                task: task
            })
        }
    });
};