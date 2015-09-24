/**
 * Created by Bar Wachtel on 20/09/2015.
 */
var mongoose = require("mongoose");
var dbConnection = require("../modules/db-connection");

var userSchema = mongoose.Schema({
    username: {
        type: String,
        required: true,
        unique: true
    },
    password: {
        type: String,
        required: true
    },
    accessToken: String
});

// Schema.methods = document methods (available on Objects)
userSchema.methods.create = function (user, cb) {
    var newUser = new User(user);
    newUser.save(cb);
};

userSchema.methods.passwordMatches = function (password) {
    return this.password === password;
};

// Schema.statics = static methods (available on Model)
userSchema.statics.findByName = function (username, cb) {
    User.findOne({username: username}, cb);
};

userSchema.statics.get = function (query, cb) {
    User.findOne(query, cb);
};

var User = dbConnection.model('User', userSchema);

module.exports = User;