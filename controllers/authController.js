var jwt = require('jsonwebtoken');
var config = require('../config');
var httpStatusCodes = require('../httpStatusCodes');
var User = require('../models/User');
var logger = require('../modules/logger');

exports.authToken = function (req, res, next) {
    var token = req.body.token || req.query.token || req.headers['x-access-token'];

    if (token) {
        jwt.verify(token, config.secret, function (err, decoded) {
            if (err) {
                err.status = httpStatusCodes.unauthorized;
                next(err);
            } else {
                // Token contains user db object id (not all routes require getting user from db)
                req.userId = decoded.userId;
                next();
            }
        })
    } else {
        var err = new Error('No token provided.');
        err.status = httpStatusCodes.unauthorized;
        next(err);
    }
};

exports.attachUserToRequest = function (req, res, next) {
    User.get({_id: req.userId }, function (err, user) {
        if (err) {
            logger.error(err);
            err.status = httpStatusCodes.internalError;
            next(err);
        } else {
            if (user) {
                req.user = user;
                next();
            } else {
                logger.error("No user found!");
                var err = new Error('No user found!');
                err.status = httpStatusCodes.internalError;
                next(err);
            }
        }
    })
};
