/**
 * User.js
 *
 * @description :: TODO: You might write a short summary of how this model works and what it represents here.
 * @docs        :: http://sailsjs.org/#!documentation/models
 */

var bcrypt = require('bcrypt');

module.exports = {

  attributes: {
    email: {
      type: 'email',
      required: true,
      unique: true
    },
    username: {
      type: 'string',
      required: true,
      unique: true
    },
    accessToken: {
      type: 'string'
    },
    firstName: {
      type: 'string'
    },
    lastName: {
      type: 'string'
    },
    socialNetworkId: {
      type: 'integer'
    },
    socialId: {
      type: 'string'
    },
    socialAccessToken: {
      type: 'string'
    },
    isAdmin: {
      type: 'boolean'
    },
    password: {
      type: 'string',
      minLength: 6,
      required: true
    },
    //TODO socialNetworkId + socialId should be unique-couple.

    toJSON: function () {
      var obj = this.toObject();
      delete obj.password;
      return obj;
    }
  },
  beforeCreate: function (user, cb) {
    bcrypt.genSalt(10, function (err, salt) {
      bcrypt.hash(user.password, salt, function (err, hash) {
        if (err) {
          console.log(err);
          cb(err);
        } else {
          user.password = hash;
          cb();
        }
      });
    });
  },
  findBySocialId: function (id, cb) {
    User.findOne({id: 1}).exec(cb);
  }
};
