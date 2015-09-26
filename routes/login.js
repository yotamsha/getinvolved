var express = require('express');
var router = express.Router();

var passport = require('passport');
var loginController = require('../controllers/loginController');

/* Post login info . */
router.get('/', function (req, res, next) {
    res.render('login', {title: 'getInvolved'});
});

router.post('/',
    passport.authenticate('local', {session: false}),
    loginController.userLogin
);

router.post('/createUser',
    loginController.createUser,
    loginController.userLogin);

module.exports = router;