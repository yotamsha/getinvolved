/**
 * Created by Bar Wachtel on 25/09/2015.
 */
var config = require('../config.js');
var jwt = require('jsonwebtoken');
var User = require('../models/User');

exports.returnAccessToken = function (req, res, next) {
    var token = generateToken(req.user);

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
    })
};

function generateToken(details) {
    //Encode mongo user id
    return jwt.sign({
            userId: details._id,
            timestamp: new Date().getMilliseconds()
        }, config.secret,
        {
            //options
        })
}