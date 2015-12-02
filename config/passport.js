var passport = require('passport');
var JwtStrategy = require('passport-jwt').Strategy;

var LocalStrategy = require('passport-local').Strategy;
var FacebookStrategy = require('passport-facebook').Strategy;
var FacebookTokenStrategy = require('passport-facebook-token');

//TODO: Put password hashing/validation in CipherService
var bcrypt = require('bcrypt');

var EXPIRES_IN_MINUTES = 60 * 24;
var SECRET = process.env.tokenSecret || "Ojk5MiwiaWF0IjoxNDQ5MDkwNjgzfQ0JcoJgkZD8YTqNf";
var ALGORITHM = "HS256";
var ISSUER = "getinvolved.org.il";
var AUDIENCE = "getinvolved.org.il";

var JWT_STRATEGY_CONFIG = {
  secretOrKey: SECRET,
  issuer: ISSUER,
  audience: AUDIENCE,
  passReqToCallback: false
};


var FACEBOOK_STRATEGY_CONFIG = {
  clientID: "855279301236291",
  clientSecret: "99df83a3f04e1e6d14191a781381f1af",
  enableProof: false,
  profileFields: ["id", "name", "email"]
};

var socialNetworkIds = {
  facebook: 0
};

function _onJwtStrategyAuth(payload, next) {
  var user = payload.user;
  return next(null, user, {});
}

function _onFacebookStrategyAuth(accessToken, refreshToken, profile, done) {
  //TODO: Email is required field, need to make sure its returned in facebook profile
  User.findBySocialId(profile.id, function (err, user) {
    if (err || user[0]) {
      return done(err, user[0]); // either will do
    } else {
      // if there is no user found with that facebook id, create them
      var newUser = {};

      console.log(profile);
      // set all of the facebook information in our user model
      newUser.username = FacebookService.generateFacebookUsername(profile);
      newUser.password = FacebookService.generateRandomString();

      newUser.firstName = FacebookService.getFirstName(profile);
      newUser.lastName = FacebookService.getLastName(profile);
      newUser.socialNetworkId = socialNetworkIds.facebook;
      newUser.socialId = profile.id;
      newUser.socialAccessToken = accessToken;
      if (profile.emails && profile.emails[0]) {
        newUser.email = profile.emails[0].value;
      }

      console.log("Users email " + newUser.email);
      User.create(newUser, done);
    }
  });
}

passport.use(
  new JwtStrategy(JWT_STRATEGY_CONFIG, _onJwtStrategyAuth));

passport.use(new FacebookTokenStrategy(FACEBOOK_STRATEGY_CONFIG, _onFacebookStrategyAuth));

passport.use(new LocalStrategy({
    usernameField: 'email',
    passwordField: 'password'
  },
  function(email, password, done) {
    User.findOne({ email: email }, function (err, user) {
      if (err) { return done(err); }
      if (!user) {
        return done(null, false, { message: 'Incorrect email.' });
      }

      bcrypt.compare(password, user.password, function (err, res) {
        if (!res)
          return done(null, false, {
            message: 'Invalid Password'
          });
        return done(null, user, {
          message: 'Logged In Successfully'
        });
      });
    });
  }
));

//passport.use(new FacebookStrategy(
//  {
//    clientID: sails.config.facebook.appId,
//    clientSecret: sails.config.facebook.appSecret,
//    callbackURL: sails.config.facebook.callbackUrl
//  },
//  _onFacebookStrategyAuth
//));

module.exports.jwtSettings = {
  expiresInMinutes: EXPIRES_IN_MINUTES,
  secret: SECRET,
  algorithm : ALGORITHM,
  issuer : ISSUER,
  audience : AUDIENCE
};

