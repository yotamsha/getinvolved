var express = require('express');
var router = express.Router();
var authController = require('../controllers/authController');
var userController = require('../controllers/userController');
var loginController = require('../controllers/loginController');
var passport = require('passport');

// get user
router.get('/',
    authController.authToken,
    authController.attachUserToRequest,
    userController.getUser
);

// update user
router.post('/',
    authController.authToken,
    userController.updateUser
);

// create user
router.post('/create',
    userController.createUser,
    loginController.returnAccessToken
);

// login using local strategy
router.post('/',
    passport.authenticate('local', {session: false}),
    loginController.returnAccessToken
);

// login using facebook access token
router.post('/facebook',
    passport.authenticate('facebook-token'),
    loginController.returnAccessToken
);

//// facebook login
//router.get('/facebook',
//    passport.authenticate('facebook', {session: false, scope: 'email'})
//);
//
//// facebook callback endpoint
//router.get('/facebookcallback',
//    passport.authenticate('facebook', {session: false}),
//    loginController.returnAccessToken
//);

module.exports = router;
