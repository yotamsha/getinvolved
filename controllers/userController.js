var User = require('../models/User');
var authController = require('../controllers/authController');

/**
 * Created by Bar Wachtel on 26/09/2015.
 */
exports.getUser = function (req, res, next) {
    if (!req.user && req.userId) {
        authController.addUserToReq(req, res, function () {
            res.json({
                success: true,
                user: req.user
            });
        })
    } else {
        res.json({
            success: true,
            user: req.user
        });
    }
};

exports.update = function (req, res, next) {
    // Better to get the user object, validate updates and save to database ;]
    console.log(req.body);
    console.log(req.params);
    console.log(req.query);

    if (req.user) {
        req.user.update(JSON.parse(req.query.user), function(err) {
            if (err) {
                res.json({
                   success: false
                });
            } else {
                res.json({
                    success: true
                });
            }
        })
    } else {
        User.getAndUpdate({ _id: req.userId }, JSON.parse(req.query.user), function(err) {
            if (err) {
                res.json({
                    success: false
                });
            } else {
                res.json({
                    success: true
                });
            }
        });
    }
};