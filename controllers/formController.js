var Form = require("../models/Form");

exports.createUserForm = function (req, res, next) {
    Form.create(req.body, function (err) {
        if (err) {
            next(err);
        } else {
            res.json({
                success: true,
                message: "User form saved"
            });
        }
    });
};

exports.getAllForms = function (req, res, next) {
    Form.getAll(function (err, forms) {
        if (err) {
            next(err);
        } else {
            res.json({
                success: true,
                message: "All user forms",
                forms: forms
            });
        }
    });
};
