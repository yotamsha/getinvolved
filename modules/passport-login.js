/**
 * Created by Bar Wachtel on 21/09/2015.
 */
var passport = require('passport');
var LocalStrategy = require('passport-local').Strategy;
var FacebookStrategy = require('passport-facebook').Strategy;
var config = require('../config');
var User = require('../models/User');
var logger = require('./logger');

var socialNetworkIds = {
    facebook: 0
}

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
        User.findByName(getFacebookUsername(profile), function(err, user) {
            // if there is an error, stop everything and return that
            // ie an error connecting to the database
            if (err)
                return done(err);

            // if the user is found, then log them in
            if (user) {
                return done(null, user); // user found, return that user
            } else {
                // if there is no user found with that facebook id, create them
                var newUser = {};

                // set all of the facebook information in our user model
                newUser.username = getFacebookUsername(profile);
                newUser.password = createFacebookUserPassword();

                newUser.firstName = getFirstName(profile.displayName);
                newUser.lastName = getLastName(profile.displayName);
                newUser.socialNetworkId = socialNetworkIds.facebook;
                newUser.socialId = profile.id;
                newUser.socialToken = token;
                //newUser.email = profile.emails[0].value;

                User.create(newUser, function(err, user) {
                    if (err) {
                        throw err;
                    } else {
                        // if successful, return the new user
                        return done(null, user);
                    }
                });
            }
        });
    }
));

function getFacebookUsername(profile) {
    return getFirstName(profile.displayName) + profile.id;
}

function getFirstName(displayName) {
    return displayName.split(' ')[0];
}

function getLastName(displayName) {
    var names = displayName.split(' ');
    var lastName = "";
    if (names.length >= 1) {
        lastName = names[names.length - 1];
    }
    return lastName;
}

function createFacebookUserPassword() {
    // Since password is a required field, but could allow the user to login later
    return Math.random().toString(36).substring(7);
}

module.exports = passport;