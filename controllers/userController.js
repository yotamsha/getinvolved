var User = require('../models/User');
var authController = require('../controllers/authController');
var passport = require('passport');

/**
 * Created by Bar Wachtel on 26/09/2015.
 */
exports.getUser = function (req, res, next) {
    if (!req.user && req.userId) {
        authController.attachUserToRequest(req, res, function () {
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

exports.updateUser = function (req, res, next) {
    // Better to get the user object, validate updates and save to database ;]
    if (req.user) {
        req.user.update(JSON.parse(req.query.update), function (err) {
            if (err) {
                next(err);
            } else {
                res.json({
                    success: true,
                    message: "User update succeeded"
                });
            }
        })
    } else {
        next(new Error('Expected user attached to request'));
    }
};

exports.createAndLogin = function (req, res, next) {
    if (req.body.username) {
        _localCreateAndLogin(req, res, next);
    } else if (req.query.access_token) {
        _facebookCreateAndLogin(req, res, next);
    } else {
        next(new Error("Not enough parameters supplied"));
    }

};

exports.deleteUser = function (req, res, next) {
    if (req.query.userId) {
        User.removeById(req.query.userId, function (err) {
            if (err) {
                next(err);
            } else {
                res.json({
                    success: true,
                    message: "Removed user"
                });
            }
        });
    }
};

exports.getUserTasks = function (req, res, next) {
    if (req.user) {
        req.user.getTasks(req.user._id, function (err, _tasks) {
            console.log(_tasks);
            res.json({
                success: true,
                tasks: _tasks
            })
        });
    }
};

function _localCreateAndLogin(req, res, next) {
    User.findOrCreate(
        {username: req.body.username},
        {password: req.body.password},
        function (err, user, created) {
            if (err) {
                next(err);
            } else if (!created) {
                if (user.passwordMatches(req.body.password)) {
                    req.user = user;
                } else {
                    next(new Error('Password doesn\'t match'));
                }
            } else {
                req.user = user;
            }
            next();
        })
}

function _facebookCreateAndLogin(req, res, next) {
    passport.authenticate('facebook-token', {session: false})(req, res, next);
}
