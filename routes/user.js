var express = require('express');
var router = express.Router();
var authController = require('../controllers/authController');
var userController = require('../controllers/userController');
var loginController = require('../controllers/loginController');
//var passport = require('passport');

// create & login user
router.put('/',
    userController.createAndLogin,
    loginController.returnAccessToken
);

// get user
router.get('/',
    authController.authToken,
    authController.attachUserToRequest,
    userController.getUser
);

// update user
router.post('/',
    authController.authToken,
    authController.attachUserToRequest,
    userController.updateUser
);

router.delete('/',
    authController.authToken,
    authController.attachUserToRequest,
    authController.userIsAdmin,
    userController.deleteUser
);

router.get('/task',
    authController.authToken,
    authController.attachUserToRequest,
    userController.getUserTasks
);

// create user
//router.post('/create',
//    userController.createUser,
//    loginController.returnAccessToken
//);

// login using local strategy
//router.post('/',
//    passport.authenticate('local', {session: false}),
//    loginController.returnAccessToken
//);

// login using facebook access token
//router.post('/facebook',
//    passport.authenticate('facebook-token', { session: false }),
//    loginController.returnAccessToken
//);

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
