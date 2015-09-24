var express = require('express');
var router = express.Router();
var passport = require('passport');
var jwt = require('jsonwebtoken');
var config = require('../config');

router.get('/', passport.authenticate('facebook', {session: false, scope: 'email'}));

// User should be returned a jsonwebtoken
router.get('/callback', passport.authenticate('facebook', {session: false}),
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

function getToken(details) {
    return jwt.sign(details, config.secret, {
        expiresInMinutes: 600
    })
}

module.exports = router;