/**
 * Created by Bar Wachtel on 21/09/2015.
 */
var passport = require('passport');
var LocalStrategy = require('passport-local').Strategy;
var FacebookStrategy = require('passport-facebook').Strategy;
var config = require('../config');
var User = require('../models/User');
var logger = require('./logger');


passport.use(new LocalStrategy(
    function(username, password, done) {
        // Should authenticate against users in database
        User.get({username: username}, function(err, user) {
            if (err) {
                logger.error(err);
            } else {
                if (user && user.passwordMatches(password)) {
                    return done(null, user);
                } else {
                    logger.log("No user named " + username);
                }
            }
        });
    }
));

passport.use(new FacebookStrategy(
    {
        clientID: config.facebook.appId,
        clientSecret: config.facebook.appSecret,
        callbackURL: config.facebook.callbackUrl
    },
    function(token, refreshToken, profile, done) {
        // Should authenticate user against db
        if (profile) {
            done(null, {
                name: "Jim James"
            })
        }

        // Else clause - create user and login
    }
));

module.exports = passport;