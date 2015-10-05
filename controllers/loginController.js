/**
 * Created by Bar Wachtel on 25/09/2015.
 */
var config = require('../config.js');
var jwt = require('jsonwebtoken');
var User = require('../models/User');

exports.returnAccessToken = function (req, res, next) {
    if (req.user) {
        var token = generateToken(req.user);

        req.user.update({
            accessToken: token
        }, function (err) {
            if (err) {
                next(err);
            } else {
                res.json({
                    success: true,
                    token: token
                });
            }
        })
    } else {
        logger.error('No user attached to request');
        next(new Error("Internal error"));
    }
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