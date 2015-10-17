var config = {
    secret: "topSecret",
    facebook: {
        appId: "855279301236291",
        appSecret: "99df83a3f04e1e6d14191a781381f1af",
        callbackUrl: "user/facebookcallback",
        nada: 'nada'
    },
    //mongodb: {
    //    host: 'localhost',
    //    dbName: 'getInvolved'
    //}
    mongodb: {
        host: "baz:baz@ds041164.mongolab.com:41164/heroku_c71zd0vr",
        dbName: "getInvolved"
    }
};

module.exports = config;