var express = require('express');
var router = express.Router();
var authController = require('../controllers/authController');
var userController = require('../controllers/userController');

/* GET users listing. */
router.get('/',
    authController.auth,
    authController.addUserToReq,
    userController.getUser
);

router.post('/',
    authController.auth,
    userController.update
);

module.exports = router;
