/**
 * Case.js
 *
 * @description :: TODO: You might write a short summary of how this model works and what it represents here.
 * @docs        :: http://sailsjs.org/#!documentation/models
 */

module.exports = {
  autoCreatedAt: false,
  autoUpdatedAt: false,
  attributes: {
    name: {
      type: 'string'
    },
    city: {
      type: 'string'
    },
    immediate: {
      type: 'boolean'
    },
    status: {
      type: 'string',
      enum: ['pendingApproval', 'pendingInvolvement', 'partiallyAssigned', 'fullyAssigned',
        'partiallyCompleted', 'completed', 'cancelledByUser', 'cancelledByAdmin',
        'missingInfo', 'rejected', 'overdue'],
      defaultsTo: 'pendingApproval'
    },
    tasks: {
      collection: 'Task',
      via: 'relatedToCase'
    },
    petitioner: {
      model: 'User'
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

