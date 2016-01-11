/**
 * User.js
 *
 * @description :: TODO: You might write a short summary of how this model works and what it represents here.
 * @docs        :: http://sailsjs.org/#!documentation/models
 */

var bcrypt = require('bcrypt');

module.exports = {
  autoCreatedAt: false,
  autoUpdatedAt: false,

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
    password: {
      type: 'string',
      minLength: 6
      //required: true -- user joining from facebook never needs to provide a password!
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
    volunteerTasks: {
      collection : 'Task',
      via : 'volunteers'
    },
    petitionerCases: {
      collection: 'Case',
      via: 'petitioner'
    },
    creationDate: {
      columnName: 'creationDate',
      type: 'integer',
      defaultsTo: function () {
        return new Date().getTime();
      }
    },
    updateDate: {
      columnName: 'updateDate',
      type: 'integer',
      defaultsTo: function () {
        return new Date().getTime();
      }
    },

    // Object (instance) methods go here
    toJSON: function () {
      var obj = this.toObject();
      delete obj.password;
      return obj;
    },
    passwordMatches: function(_password) {
      return this.password === _password;
    },
    updateMe: function(opts, cb) {
      var updateKeys = Object.keys(opts);
      updateKeys.forEach(function(key) {
        console.log("updating " + key + " to value " + opts[key]);
        if (attributeCanBeUpdatedByUser(key)) {
          this[key] = opts[key];
        }
      });
      this.save(cb);
    }
  },
  beforeUpdate: function (values, next) {
    values.updateDate = new Date().getTime();
    next();
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

function attributeCanBeUpdatedByUser(key) {
  // Some values should not be updateable!
  return true;
}
