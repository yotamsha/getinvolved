var express = require('express');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var passport = require('passport');
var LocalStrategy = require('passport-local').Strategy;
var FacebookStrategy = require('passport-facebook').Strategy;
var config = require("./config");

var routes = require('./routes/index');
var users = require('./routes/users');
var login = require('./routes/login');
var authed = require('./routes/authed');
var facebook = require('./routes/facebook')

var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

// uncomment after placing your favicon in /public
//app.use(favicon(__dirname + '/public/favicon.ico'));
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));
app.use(passport.initialize()); // Important!

app.use('/', routes);
app.use('/users', users);
app.use('/login', login);
app.use('/authed', authed);
app.use('/facebook', facebook);

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

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  var err = new Error('Not Found');
  err.status = 404;
  next(err);
});

// error handlers

// development error handler
// will print stacktrace
if (app.get('env') === 'development') {
  app.use(function(err, req, res, next) {
    res.status(err.status || 500);
    res.render('error', {
      message: err.message,
      error: err
    });
  });
}

// production error handler
// no stacktraces leaked to user
app.use(function(err, req, res, next) {
  res.status(err.status || 500);
  res.render('error', {
    message: err.message,
    error: {}
  });
});


module.exports = app;
