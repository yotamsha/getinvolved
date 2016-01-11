/**
* Task.js
*
* @description :: TODO: You might write a short summary of how this model works and what it represents here.
* @docs        :: http://sailsjs.org/#!documentation/models
*/

module.exports = {
  autoCreatedAt: false,
  autoUpdatedAt: false,
  attributes: {
    name: 'string',
    relatedToCase: {
      model: 'Case'
    },
    volunteers: {
      collection: 'User',
      via: 'volunteerTasks'
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
    }
  },
  beforeUpdate: function (values, next) {
    values.updateDate = new Date().getTime();
    next();
  }
};

