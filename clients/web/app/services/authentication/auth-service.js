/**
 * Created by yotam on 28/1/2016.
 */
/**
 * Created by yotam on 29/1/2016.
 */
'use strict';

angular.module('app.services.authentication.auth-service', [])
    .service('AuthService', ['Restangular', '$rootScope', '$cookieStore', '$http', '$timeout',
        function (Restangular, $rootScope, $cookieStore, $http, $timeout) {
            var facebookAuthenticator = {

                watchAuthenticationStatusChange: function () {

                    var _self = this;

                    FB.Event.subscribe('auth.authResponseChange', function (res) {

                        if (res.status === 'connected') {
                            /*
                             The user is already logged,
                             is possible retrieve his personal info
                             */
                            _self.getUserInfo();

                            /*
                             This is also the point where you should create a
                             session for the current user.
                             For this purpose you can use the data inside the
                             res.authResponse object.
                             */

                        }
                        else {

                            /*
                             The user is not logged to the app, or into Facebook:
                             destroy the session on the server.
                             */

                        }

                    });

                },
                getUserInfo: function () {
                    var _self = this;
                    FB.getLoginStatus(function (response) {
                        if (response.authResponse) {
                            console.log(response.authResponse);
                            _self.signup(response.authResponse);
                        } else {
                            // do something...maybe show a login prompt
                        }
                    });

                    /*                    FB.api('/me', function(res) {

                     $rootScope.$apply(function() {
                     //alert("fb logged in");
                     console.log("facebook login completed: " +res);
                     $rootScope.user = _self.user = res;

                     });

                     })*/
                    ;

                },
                login: function () {

                },
                signup: function (authResponse) {
                    var newUser = {
                        /*                        "first_name": "One",
                         "last_name": "User",
                         "user_name": "one_user@gi.net",
                         "email": "one_user@gi.net",
                         "facebook_id": "1234567890431",*/
                        "facebook_access_token": authResponse.accessToken
                        /*
                         "role": "ROLE_USER"
                         */
                    };
/*                    var baseUsers = Restangular.all('users');
                    baseUsers.post(newUser).then(function (response) {
                        console.log("response: ", response);
                    });*/
                    $http.get("http://localhost:5000/login/fb_token/" + authResponse.accessToken).success(function(response){
                        console.log(response);
                    }).error(function(error){
                        console.log(error);
                    })
                },
                logout: function () {

                    var _self = this;

                    FB.logout(function (response) {

                        $rootScope.$apply(function () {

                            $rootScope.user = _self.user = {};

                        });

                    });

                }

            };
            return {
                facebookAuthenticator: facebookAuthenticator

            };
        }]);
