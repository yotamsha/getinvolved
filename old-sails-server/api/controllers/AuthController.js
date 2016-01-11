/**
 * AuthController
 *
 * @description :: Server-side logic for managing auths
 * @help        :: See http://sailsjs.org/#!/documentation/concepts/Controllers
 */

var passport = require('passport');
var jwt = require('jsonwebtoken');
module.exports = {

  _config: {
    actions: false,
    shortcuts: false,
    rest: false
  },

  login: function (req, res, next) {
      console.log(" in createAndLogin");
      if (req.param("email") && req.param("password")) {
        req.body.email = req.param("email");
        req.body.password = req.param("password");
        passport.authenticate('local', {session: false})(req, res, next);
      } else if (req.param("access_token")) {
        req.query.access_token = req.param("access_token");
        passport.authenticate('facebook-token', {scope: FacebookService.profileFields, session: false})(req, res, next);
      } else {
        next(new Error("Not enough parameters supplied"));
      }
    },

  logout: function (req, res) {
    req.logout();
    res.redirect('/');
  },

  returnAccessToken: function (req, res, next) {
    if (req.user) {
      var token = CipherService.createToken(req.user);

      req.user.updateMe({
        accessToken: token
      }, function (err, user) {
        if (err) {
          next(err);
        } else {
          res.json(
            {
            success: true,
            token: token
          });
        }
      })
    } else {
      sails.log.error('No user attached to request');
      next(new Error("Internal error"));
    }
    //sails.log.info(" in returnAccessToken - returning 200 ok");
    //res.send(200)
  }
};

/**
 * Sails controllers expose some logic automatically via blueprints.
 *
 * Blueprints are enabled for all controllers by default, and they can be turned on or off
 * app-wide in `config/controllers.js`. The settings below are overrides provided specifically
 * for AuthController.
 *
 * NOTE:
 * REST and CRUD shortcut blueprints are only enabled if a matching model file
 * (`models/Auth.js`) exists.
 *
 * NOTE:
 * You may also override the logic and leave the routes intact by creating your own
 * custom middleware for AuthController's `find`, `create`, `update`, and/or
 * `destroy` actions.
 */

module.exports.blueprints = {

  // Expose a route for every method,
  // e.g.
  // `/auth/foo` => `foo: function (req, res) {}`
  actions: false,

  // Expose a RESTful API, e.g.
  // `post /auth` => `create: function (req, res) {}`
  rest: false,

  // Expose simple CRUD shortcuts, e.g.
  // `/auth/create` => `create: function (req, res) {}`
  // (useful for prototyping)
  shortcuts: false

};

