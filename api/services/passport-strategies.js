///**
// * Created by Bar Wachtel on 21/09/2015.
// */
//var passport = require('passport');
//var LocalStrategy = require('passport-local').Strategy;
//var FacebookStrategy = require('passport-facebook').Strategy;
//var FacebookTokenStrategy = require('passport-facebook-token');
//
//var bcrypt = require('bcrypt');
////var config = require('../old-school/config');
////var User = require('./User');
////var logger = require('./logger');
//
//var socialNetworkIds = {
//    facebook: 0
//}
//
//passport.use(new LocalStrategy({
//    usernameField: 'email',
//    passwordField: 'password'
//  },
//  function(email, password, done) {
//    User.findOne({ email: email }, function (err, user) {
//      if (err) { return done(err); }
//      if (!user) {
//        return done(null, false, { message: 'Incorrect email.' });
//      }
//
//      bcrypt.compare(password, user.password, function (err, res) {
//        if (!res)
//          return done(null, false, {
//            message: 'Invalid Password'
//          });
//        return done(null, user, {
//          message: 'Logged In Successfully'
//        });
//      });
//    });
//  }
//));
//
//passport.use(new FacebookTokenStrategy(
//    {
//        clientID: sails.config.facebook.appId,
//        clientSecret: sails.config.facebook.appSecret,
//        enableProof: false,
//        profileFields :
//          FacebookService.profileFields
//    },
//    function (accessToken, refreshToken, profile, done) {
//      //TODO: Email is required field, need to make sure its returned in facebook profile
//        User.findBySocialId(profile.id, function (err, user) {
//            if (err || user[0]) {
//                return done(err, user[0]); // either will do
//            } else {
//                // if there is no user found with that facebook id, create them
//                var newUser = {};
//
//                console.log(profile);
//                // set all of the facebook information in our user model
//                newUser.username = FacebookService.generateFacebookUsername(profile);
//                newUser.password = FacebookService.generateRandomString();
//
//                newUser.firstName = FacebookService.getFirstName(profile);
//                newUser.lastName = FacebookService.getLastName(profile);
//                newUser.socialNetworkId = socialNetworkIds.facebook;
//                newUser.socialId = profile.id;
//                newUser.socialAccessToken = accessToken;
//                if (profile.emails && profile.emails[0]) {
//                    newUser.email = profile.emails[0].value;
//                }
//
//                console.log("Users email " + newUser.email);
//                User.create(newUser, done);
//            }
//        });
//    }
//));
//
//passport.use(new FacebookStrategy(
//    {
//        clientID: sails.config.facebook.appId,
//        clientSecret: sails.config.facebook.appSecret,
//        callbackURL: sails.config.facebook.callbackUrl
//    },
//    function (token, refreshToken, profile, done) {
//        User.findBySocialId(profile.id, function (err, user) {
//            // if there is an error, stop everything and return that
//            // ie an error connecting to the database
//            if (err)
//                return done(err);
//
//            // if the user is found, then log them in
//            if (user) {
//                return done(null, user); // user found, return that user
//            } else {
//                // if there is no user found with that facebook id, create them
//                var newUser = {};
//
//                // set all of the facebook information in our user model
//                newUser.username = generateFacebookUsername(profile);
//                newUser.password = generateRandomString();
//
//                newUser.firstName = getFirstName(profile.displayName);
//                newUser.lastName = getLastName(profile.displayName);
//                newUser.socialNetworkId = socialNetworkIds.facebook;
//                newUser.socialId = profile.id;
//                newUser.socialAccessToken = token;
//                //newUser.email = profile.emails[0].value;
//
//                User.create(newUser, function (err, user) {
//                    if (err) {
//                        throw err;
//                    } else {
//                        // if successful, return the new user
//                        return done(null, user);
//                    }
//                });
//            }
//        });
//    }
//));
//
//module.exports = passport;
