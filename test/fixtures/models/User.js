/**
 * Created by yotam on 17/12/2015.
 */
module.exports = {
  attributes: {
    email: {
      type: 'email',
      required: true,
      unique: true
    },
    username: {
      type: 'string',
      //required: true,
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
    tasks : {
      collection : 'task',
      via : 'participants'
    },

  }
};
