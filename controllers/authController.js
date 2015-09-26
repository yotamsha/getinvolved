var jwt = require('jsonwebtoken');
var config = require('../config');
var httpStatusCodes = require('../httpStatusCodes');
var User = require('../models/User');
var logger = require('../modules/logger');

exports.auth = function (req, res, next) {
    var token = req.body.token || req.query.token || req.headers['x-access-token'];

    if (token) {
        jwt.verify(token, config.secret, function (err, decoded) {
            if (err) {
                return res.status(httpStatusCodes.unauthorized).json({
                    success: false,
                    message: 'Failed to authenticate token'
                });
            } else {
                // Token contains user db object id (not all routes require getting user from db)
                req.userId = decoded.userId;
                next();
            }
        })
    } else {
        return res.status(httpStatusCodes.unauthorized).send({
            success: false,
            message: 'No token provided.'
        });
    }
};

exports.addUserToReq = function (req, res, next) {
    User.get({_id: req.userId }, function (err, user) {
        if (err) {
            logger.error(err);
            return res.status(httpStatusCodes.internalError).json({
                success: false,
                message: 'Error in database'
            });
        } else {
            if (user) {
                req.user = user;
                next();
            } else {
                logger.error("No user found!");
                return res.status(httpStatusCodes.internalError).json({
                    success: false,
                    message: 'No user found!'
                });
            }
        }
    })
};
