var express = require('express');
var router = express.Router();
var passport = require('passport');
var loginController = require('../controllers/loginController');

router.get('/', passport.authenticate('facebook', {session: false, scope: 'email'}));

router.get('/callback',
    passport.authenticate('facebook', {session: false}),
    loginController.userLogin);

module.exports = router;