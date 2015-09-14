var express = require('express');
var router = express.Router();
var jwt = require('jsonwebtoken');
var config = require('../config');

router.use('*', function(req, res, next) {
    var token = req.body.token || req.query.token || req.headers['x-access-token'];

    if (token) {
        jwt.verify(token, config.secret, function(err, decoded) {
            if (err) {
                return res.json({
                    success: false,
                    message: 'Failed to authenticate token'
                });
            } else {
                // Check if specified user has token in database
                req.decoded = decoded;
                next();
            }
        })
    } else {
        return res.status(403).send({
            success: false,
            message: 'No token provided.'
        });
    }
});

router.get('/', function(req, res, next) {
   res.json({
       decodedToken: req.decoded
   });
});

module.exports = router;