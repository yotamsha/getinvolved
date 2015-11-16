/*

*/
/**
 * SwaggerController
 *
 * @description :: Server-side logic for managing swaggers
 * @help        :: See http://sailsjs.org/#!/documentation/concepts/Controllers
 *//*



var _ = require('lodash');
var _super = require('sails-swagger/dist/api/controllers/SwaggerController');

_.merge(exports, _super);
_.merge(exports, {

  // Extend with custom logic here by adding additional fields, methods, etc.

});
*/
/*
module.exports = {
  _config: {
    actions: false,
      shortcuts: false,
      rest: false
  },
}
*//*


module.exports.blueprints = {

  // Expose a route for every method,
  // e.g.
  // `/auth/foo` => `foo: function (req, res) {}`
  actions: true,

  // Expose a RESTful API, e.g.
  // `post /auth` => `create: function (req, res) {}`
  rest: false,

  // Expose simple CRUD shortcuts, e.g.
  // `/auth/create` => `create: function (req, res) {}`
  // (useful for prototyping)
  shortcuts: false

};
*/
