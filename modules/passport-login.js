/**
 * Created by Bar Wachtel on 21/09/2015.
 */
var passport = require('passport');
var LocalStrategy = require('passport-local').Strategy;
var FacebookStrategy = require('passport-facebook').Strategy;
var config = require('../config');


passport.use(new LocalStrategy(
    function(username, password, done) {
        // Should authenticate against users in database
        // SELECT * FROM Users WHERE username = username AND password = password;
        if (username === 'bazza' && password === 'wazza') {
            return done(null, {
                name: 'Bar Wachtel'
            })
        } else {
            return done(null, false, { message: "Wrong username or password"});
        }
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