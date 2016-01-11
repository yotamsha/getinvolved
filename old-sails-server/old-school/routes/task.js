var express = require('express');
var router = express.Router();
//var authController = require('../controllers/authController');
var taskController = require('./taskController');

router.get('/', taskController.getTasks);

router.put('/', taskController.createTask);

module.exports = router;