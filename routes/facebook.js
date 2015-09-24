var express = require('express');
var router = express.Router();
var passport = require('passport');
var jwt = require('jsonwebtoken');

router.get('/', passport.authenticate('facebook', { session: false, scope: 'email' }));

// User should be returned a jsonwebtoken
router.get('/callback', passport.authenticate('facebook', {
    successRedirect: '/authed',
    failureRedirect: '/login',
    session: false
}));

module.exports = router;