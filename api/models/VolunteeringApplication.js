/**
 * VolunteeringApplication.js
 *
 * @description :: TODO: You might write a short summary of how this model works and what it represents here.
 * @docs        :: http://sailsjs.org/#!documentation/models
 */
var CONSTS = require("./../services/consts");
module.exports = {

  attributes: {
    firstName: {
      type: 'string'
    },
    lastName: {
      type: 'string'
    },
    email: {
      type: 'email'
    },
    phoneNumber: {
      type: 'string'
    },
    lastName: {
      type: 'string'
    },
    volunteerArea: {
      type: 'string'
    },
    volunteerDate: {
      type: 'date'
    },
    sex: {
      type: 'string',
      enum: ['MALE', 'FEMALE']
    }

  },
  beforeValidate: function (application, cb) {
    if (!application.email && !application.phoneNumber) {

      cb({
        code: CONSTS.ERROR_CODES.INVALID_INPUT_EMAIL_OR_PHONE_MISSING.code,
        error: CONSTS.ERROR_CODES.INVALID_INPUT_EMAIL_OR_PHONE_MISSING.text
      })
    } else {
      cb();
    }
  }
};

