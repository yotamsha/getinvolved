


/**
 * SwaggerController
 *
 * @description :: Server-side logic for managing swaggers
 * @help        :: See http://sailsjs.org/#!/documentation/concepts/Controllers
 */


var _ = require('lodash');
var _super = require('sails-swagger/dist/api/controllers/SwaggerController');

_.merge(exports, _super);
_.merge(exports, {

  // Extend with custom logic here by adding additional fields, methods, etc.
  _config: {
    actions: false,
    shortcuts: false,
    rest: false
  }
});


