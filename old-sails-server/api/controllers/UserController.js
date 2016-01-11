/**
 * UserController
 *
 * @description :: Server-side logic for managing users
 * @help        :: See http://sailsjs.org/#!/documentation/concepts/Controllers
 */

//var bcrypt = require('bcrypt');
var passport = require('passport');
// var User = require('../models/User'); -- Can add this for clarity, although its not required

module.exports = {
  _config: {
    actions: false,
    shortcuts: false,
    rest: true
  }
  //attributes: {
  //  email: {
  //    type: 'email',
  //    required: true,
  //    unique: true
  //  },
  //  password: {
  //    type: 'string',
  //    minLength: 6,
  //    required: true
  //  },
  //
  //  toJSON: function () {
  //    var obj = this.toObject();
  //    delete obj.password;
  //    return obj;
  //  }
};
  //beforeCreate: function (user, cb) {
  //  bcrypt.genSalt(10, function (err, salt) {
  //    bcrypt.hash(user.password, salt, function (err, hash) {
  //      if (err) {
  //        console.log(err);
  //        cb(err);
  //      } else {
  //        user.password = hash;
  //        cb();
  //      }
  //    });
  //  });
  //}

  //test: function (req, res, next) {
  //  User.findBySocialId(null, function (err, user) {
  //    if (err) {
  //      res.json(500, err);
  //    } else {
  //      res.json(200, user);
  //    }
  //  });
  //},

  //createAndLogin: function (req, res, next) {
  //  console.log(" in createAndLogin");
  //  if (req.body.username) {
  //    _localCreateAndLogin(req, res, next);
  //  } else if (req.query.access_token) {
  //    _facebookCreateAndLogin(req, res, next);
  //  } else {
  //    next(new Error("Not enough parameters supplied"));
  //  }
  //}

//
//function _localCreateAndLogin(req, res, next) {
//  User.findOrCreate(
//    {
//      // Query
//      username: req.body.username
//    },
//    {
//      // To create
//      username: req.body.username,
//      password: req.body.password,
//      email: req.body.email
//    },
//    function (err, user) {
//      if (err) {
//        next(err);
//      }
//      if (user.passwordMatches(req.body.password)) {
//        req.user = user;
//      } else {
//        next(new Error('Password doesn\'t match'));
//      }
//      next();
//    });
//}
//
//function _facebookCreateAndLogin(req, res, next) {
//  passport.authenticate('facebook-token', {session: false})(req, res, next);
//}
