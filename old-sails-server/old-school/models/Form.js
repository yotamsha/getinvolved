/**
 * Created by Bar Wachtel on 01/11/2015.
 */
var mongoose = require("mongoose");
var dbConnection = require("../modules/db-connection");

var formSchema = mongoose.Schema({
    name: String,
    volunteerDate: Date,
    volunteerArea: String,
    updated_at: Date
});

formSchema.pre('save', function(next){
    var now = new Date();
    if ( !this.created_at ) {
        this.created_at = now;
    }
    next();
});


formSchema.statics.create = function (form, cb) {
    var newForm = new Form(form);
    newForm.save(cb);
};

formSchema.statics.getAll = function(cb) {
    Form.find({}, cb);
};


var Form = dbConnection.model('Form', formSchema);

module.exports = Form;