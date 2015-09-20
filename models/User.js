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
}

userSchema.methods.find = function(query, cb) {
    User.findOne(query, function(err, user) {
        if (err) {

        }
    })
}

var User = mongoose.model('User', userSchema);

module.export = User;