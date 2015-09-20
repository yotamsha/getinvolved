var express = require('express');
var router = express.Router();
var passport = require('passport');
var jwt = require('jsonwebtoken');
var config = require('../config.js');

/* Post login info . */
router.get('/', function(req, res, next) {
    res.render('login', { title: 'getInvolved - login' });
});

router.post('/',
    passport.authenticate('local', { session: false }),
    function (req, res, next) {
        var token = jwt.sign(req.user, config.secret, {
            expiresInMinutes: 10 * 60
        });

        res.json({
            success: true,
            token: token
        });
    });

module.exports = router;