/**
 * Created by yotam on 29/1/2016.
 */
'use strict';

angular.module('app.services.authentication.auth-service', [])
    .service('AuthService', ['Restangular', '$rootScope', '$cookieStore', '$http', 'USER_ROLES','$q',
        function (Restangular, $rootScope, $cookieStore, $http, USER_ROLES, $q) {
            var LOCAL_TOKEN_KEY = "AUTH-TOKEN";
            var _isAuthenticated = false;
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
                            _self.login(response.authResponse);
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
                login: function (authResponse) {
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
                    $http.get("http://localhost:5000/login/fb_token/" + authResponse.accessToken)
                        .success(function (response) {
                            console.log(response);
                            $http.get("http://localhost:5000/api/users" );
                            setToken();
                            storeUserCredentials(response);
                        }).error(function (error) {
                        console.log(error);
                    })
                },
                logout: function () {
                    var _self = this;
                    FB.logout(function (response) {
                        $rootScope.$apply(function () {
                            destroyUserCredentials();
                        });
                    });
                }
            };
            var _userSession = null;

            function loadUserCredentials() {
                console.log("loadUserCredentials");
                var deferred = $q.defer();
                if (_userSession){
                    deferred.resolve();
                } else {
                    var token = window.localStorage.getItem(LOCAL_TOKEN_KEY);
                    if (token) {
                        setToken();
                        // TODO add a code that retrieves the current user session with it's token.
                        // retrieve user session:
                        storeUserCredentials({});
                        deferred.resolve();
                    } else { // no token saved.
                        return deferred.reject();
                    }

                }

                return deferred.promise;

            }

            function storeUserCredentials(token) {
                _userSession = {
                    role : USER_ROLES.user
                };
                _isAuthenticated = true;
                window.localStorage.setItem(LOCAL_TOKEN_KEY, token);
                console.log("storeUserCredentials");

            }

            function setToken(token, userSession) {
                console.log("setToken");

                // Set the token as header for your requests!
                $http.defaults.headers.common['Authorization'] = token;
            }

            function destroyUserCredentials() {
                _isAuthenticated = false;
                _userSession = null;
                $http.defaults.headers.common['Authorization'] = undefined;
                window.localStorage.removeItem(LOCAL_TOKEN_KEY);
            }

            function isAuthorized(authorizedRoles) {
                console.log("isAuthorized");
                var deferred = $q.defer();
                function authorize(){
                    if (!angular.isArray(authorizedRoles)) {
                        authorizedRoles = [authorizedRoles];
                    }
                    return _isAuthenticated && authorizedRoles.indexOf(_userSession.role) !== -1
                }
                function sessionRetrieved(){
                    if (authorize()){
                        deferred.resolve();
                    } else {
                        $rootScope.$broadcast(AUTH_EVENTS.notAuthorized);
                        deferred.reject();
                    }
                }
                if (_userSession){
                    sessionRetrieved();
                } else {
                    // TODO if user is already being retrieved, no need to do it again.
                    loadUserCredentials()
                        .success(function(){
                            sessionRetrieved();
                        })
                        .error(function(){
                            deferred.reject();
                        });
                }

                return deferred.promise;
            };

            loadUserCredentials();

            return {
                facebookAuthenticator: facebookAuthenticator,
                loadUserCredentials: loadUserCredentials,
                isAuthorized: isAuthorized,
                isAuthenticated : function() {return _isAuthenticated; },
                role: function() {return _userSession && _userSession.role;}


            };
        }]);
