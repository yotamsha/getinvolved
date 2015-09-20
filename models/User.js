/**
 * Created by Bar Wachtel on 20/09/2015.
 */
var mongoose = require("mongoose");

var userSchema = mongoose.Schema({
    username: String,
    password: String,
    accessToken: String
});

userSchema.methods.findByName = function(username, cb) {
    userSchema.find({username: username}, cb);
};

userSchema.methods.find = function(query, cb) {
    // returns cb(err, user)
    User.findOne(query, cb);
};

var User = null;

module.export = function(dbConnection) {
    if (!User) {
        User = dbConnection.model('User', userSchema);
    }
    return User;
};