/**
* Task.js
*
* @description :: TODO: You might write a short summary of how this model works and what it represents here.
* @docs        :: http://sailsjs.org/#!documentation/models
*/

module.exports = {

  attributes: {
    name: {
      type: 'string'
    },
    createdAt: {
      type: 'date',
      defaultsTo: Date.now
    },
    city: {
      type: 'string'
    },
    immediate: {
      type : 'boolean'
    },
    participants : {
      collection : 'user',
      via : 'tasks'
    }

  }
};

