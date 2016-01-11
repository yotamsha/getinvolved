/**
 * Created by Bar Wachtel on 20/09/2015.
 */
var mongoose = require("mongoose");
var dbConnection = require("../modules/db-connection");
var findOrCreate = require('mongoose-findorcreate');
var Task = require("./Task");

// TODO: Add socialAccessToken to entity schema
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
    email: String,
    accessToken: String,
    firstName: String,
    lastName: String,
    socialNetworkId: Number,
    socialId: String,
    socialAccessToken: String,
    isAdmin: Boolean,
    volunteerTasks: [{type: mongoose.Schema.Types.ObjectId, ref: 'Task'}]
});

// Usage: User.findOrCreate(query, extra_data, callback(err, user, created){...});
userSchema.plugin(findOrCreate);

// Schema.methods = document methods (available on Objects)
userSchema.methods.getTasks = function (userId ,cb) {
    User.findOne({_id: userId}).populate('volunteerTasks').exec(function(err, user) {
        if (err) {
            cb(err);
        } else {
            cb(null, user.volunteerTasks);
        }
    });
};

userSchema.methods.passwordMatches = function (password) {
    return this.password === password;
};

userSchema.methods.update = function (info, cb) {
    //TODO: Validate keys exits in schema & changing legal keys (isAdmin etc.)
    var keys = Object.keys(info);

    for (var i = 0; i < keys.length; i++) {
        this[keys[i]] = info[keys[i]];
    }

    this.save(cb);
};

// Schema.statics = static methods (available on Model)
userSchema.statics.get = function (query, cb) {
    User.findOne(query, cb);
};

userSchema.statics.create = function (user, cb) {
    var newUser = new User(user);
    newUser.save(cb);
};

userSchema.statics.removeById = function (userId, cb) {
    User.findOneAndRemove({_id: userId}, cb);
};

userSchema.statics.findByName = function (username, cb) {
    User.findOne({username: username}, cb);
};

userSchema.statics.findBySocialId = function (id, cb) {
    User.findOne({socialId: id}, cb);
};

userSchema.statics.getAndUpdate = function (query, info, cb) {
    User.get(query, function (err, user) {
        if (err) {
            cb(err);
        } else {
            if (user) {
                user.update(info, cb);
            } else {
                cb(new Error("No such user exists!"));
            }
        }
    })
};

var User = dbConnection.model('User', userSchema);

module.exports = User;
