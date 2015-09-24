var express = require('express');
var router = express.Router();

var config = require('../config.js');
var passport = require('passport');
var jwt = require('jsonwebtoken');
var User = require('../models/User');

/* Post login info . */
router.get('/', function (req, res, next) {
    res.render('login', {title: 'getInvolved - login'});
});

router.post('/',
    passport.authenticate('local', {session: false}),
    function (req, res, next) {
        var token = getToken(req.user);

        req.user.update({
            accessToken: token
        }, function (err) {
            if (err) {
                // Mish mash of error handling - whats the preferred method of doing this?
                next(err);
            } else {
                res.json({
                    success: true,
                    token: token
                });
            }
        });
    });

router.post('/createUser', function (req, res, next) {
    // Validate user info
    var newUser = {
        username: req.body.username,
        password: req.body.password
    };

    User.create(newUser, function (err, user) {
        if (err) {
            res.json({
                success: false,
                error: err
            });
        } else {
            if (user) {
                var token = getToken(user);

                user.update({
                    accessToken: token
                }, function (err) {
                    if (err) {
                        // Mish mash of error handling - whats the preferred method of doing this?
                        next(err);
                    } else {
                        res.json({
                            success: true,
                            token: token
                        });
                    }
                });
            }
        }
    });

});

function getToken(details) {
    return jwt.sign(details, config.secret, {
        expiresInMinutes: 600
    })
}

module.exports = router;