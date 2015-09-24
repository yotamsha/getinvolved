/**
 * Created by Bar Wachtel on 20/09/2015.
 */
var mongoose = require("mongoose");
var dbConnection = require("../modules/db-connection");

var userSchema = mongoose.Schema({
    username: {
        type: String,
        required: true
    },
    password: {
        type: String,
        required: true
    },
    accessToken: String
});

userSchema.methods.findByName = function(username, cb) {
    userSchema.find({username: username}, cb);
};

userSchema.methods.find = function(query, cb) {
    // returns cb(err, user)
    User.findOne(query, cb);
};

userSchema.methods.create = function(user, cb) {
    var newUser = new User(user);
    newUser.save(cb);

    // Or...
    // User.create({data..}, function (err, user) {
    // });
};

userSchema.methods.passwordMatches = function(password) {
    return this.password === password;
}

var User = dbConnection.model('User', userSchema);

module.exports = User;