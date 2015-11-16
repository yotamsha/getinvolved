/**
 * Created by Bar Wachtel on 01/11/2015.
 */
var express = require('express');
var router = express.Router();
var formController = require('./formController.js');

router.post('/', formController.createUserForm);
router.get('/', formController.getAllForms);

module.exports = router;
