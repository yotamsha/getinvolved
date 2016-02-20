/**
 * Created by yotam on 29/1/2016.
 */
'use strict';

angular.module('app.services.authentication.auth-service', [])
    .service('AuthService', ['Restangular', '$rootScope', '$cookieStore', '$http', 'USER_ROLES', '$q', 'AUTH_EVENTS',
        function (Restangular, $rootScope, $cookieStore, $http, USER_ROLES, $q, AUTH_EVENTS) {
            var LOCAL_TOKEN_KEY = "AUTH-TOKEN";
            var authModel = {
                isAuthenticated: false,
                userSession: null,
                isLoading: true
            }
            var facebookAuthenticator = {
                watchAuthenticationStatusChange: function () {

                    var _self = this;

                    FB.Event.subscribe('auth.authResponseChange', function (res) {
                        console.log("fb response detected:", res);
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
                statusChangeCallback: function (response) {
                    var _self = this;
                    console.log('statusChangeCallback');
                    console.log(response);
                    // The response object is returned with a status field that lets the
                    // app know the current login status of the person.
                    // Full docs on the response object can be found in the documentation
                    // for FB.getLoginStatus().
                    if (response.status === 'connected') {
                        // Logged into your app and Facebook.
                        console.log('Already connected to FB.');
                        _self.facebookSessionRetrieved(response.authResponse);


                    } else if (response.status === 'not_authorized') {
                        // The person is logged into Facebook, but not your app.
                        console.log('Already connected to FB. But not authorized.');
                        FB.login(function (loginRes) {
                            // Handle the response object, like in statusChangeCallback() in our demo
                            // code.
                            _self.facebookSessionRetrieved(loginRes.authResponse);

                        });

                    } else {
                        // The person is not logged into Facebook, so we're not sure if
                        // they are logged into this app or not.
                        console.log('User is not logged to FB.');
                        FB.login(function (loginRes) {
                            // Handle the response object, like in statusChangeCallback() in our demo
                            // code.
                            _self.facebookSessionRetrieved(loginRes.authResponse);

                        });

                    }
                },
                /*getUserInfo: function () {
                    var _self = this;
                    FB.getLoginStatus(function (response) {
                        if (response.authResponse) {
                            console.log(response.authResponse);
                        } else {
                            // do something...maybe show a login prompt
                        }
                    });

                    /!*                    FB.api('/me', function(res) {

                     $rootScope.$apply(function() {
                     //alert("fb logged in");
                     console.log("facebook login completed: " +res);
                     $rootScope.user = _self.user = res;

                     });

                     })*!/
                    ;

                },*/
                facebookSessionRetrieved: function (authResponse) {
                    return $http.get("http://localhost:5000/login/fb_token/" + authResponse.accessToken)
                        .success(function (token) {
                            console.log(token);
                            setToken(token);
                            return $http.get("http://localhost:5000/api/users/me")
                                .success(function (user) {
                                    storeUserCredentials(token, user);
                                    $rootScope.$broadcast(AUTH_EVENTS.authenticationCompleted);
                                    return user;
                                }).error(function () {
                                    return null;
                                });

                        }).error(function (error) {
                            console.log(error);
                        })
                },
                login: function () {
                    var _self = this;
                    FB.getLoginStatus(function (response) {
                        _self.statusChangeCallback(response);
                    });


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

            function loadUserCredentials() {
                console.log("loadUserCredentials");
                var deferred = $q.defer();
                if (authModel.userSession) {
                    deferred.resolve();
                } else {
                    var token = window.localStorage.getItem(LOCAL_TOKEN_KEY);
                    if (token) {
                        setToken(token);
                        $http.get("http://localhost:5000/api/users/me")
                            .success(function (user) {
                                storeUserCredentials(null, user);
                                deferred.resolve();
                            }).error(function () {
                            deferred.reject();
                        });

                    } else { // no token saved.
                        deferred.reject();
                    }

                }

                return deferred.promise;

            }

            function storeUserCredentials(token, user) {
                console.log("storing user", user);

                authModel.userSession = user;
                authModel.isAuthenticated = true;
                if (token) {
                    window.localStorage.setItem(LOCAL_TOKEN_KEY, token);
                }

            }

            function setToken(token) {
                console.log("setToken");

                // Set the token as header for your requests!
                $http.defaults.headers.common['Authorization'] = token;
            }

            function destroyUserCredentials() {
                authModel.isAuthenticated = false;
                authModel.userSession = null;
                $http.defaults.headers.common['Authorization'] = undefined;
                window.localStorage.removeItem(LOCAL_TOKEN_KEY);
            }

            function isAuthorized(authorizedRoles) {
                console.log("isAuthorized");
                var deferred = $q.defer();

                function authorize() {
                    if (!angular.isArray(authorizedRoles)) {
                        authorizedRoles = [authorizedRoles];
                    }
                    return authModel.isAuthenticated && authorizedRoles.indexOf(authModel.userSession.role) !== -1
                }

                function sessionRetrieved() {
                    if (authorize()) {
                        deferred.resolve();
                    } else {
                        $rootScope.$broadcast(AUTH_EVENTS.notAuthorized);
                        deferred.reject();
                    }
                }

                if (authModel.userSession) {
                    sessionRetrieved();
                } else {
                    // TODO if user is already being retrieved, no need to do it again.
                    loadUserCredentials()
                        .success(function () {
                            sessionRetrieved();
                        })
                        .error(function () {
                            deferred.reject();
                        });
                }

                return deferred.promise;
            };

            loadUserCredentials().then(function () {
                // success
                authModel.isLoading = false;
            }, function () {
                // error
                authModel.isLoading = false;

            });

            return {
                facebookAuthenticator: facebookAuthenticator,
                loadUserCredentials: loadUserCredentials,
                isAuthorized: isAuthorized,
                isAuthenticated: function () {
                    return authModel.isAuthenticated;
                },
                role: function () {
                    return authModel.userSession && authModel.userSession.role;
                },
                model: function () {
                    return authModel;
                },
                logout: function () {
                    // TODO check if user is a fb user.
                    /*                    var isFacebbokUser = true;
                     if (isFacebbokUser){
                     facebookAuthenticator.logout();
                     } else {*/
                    destroyUserCredentials();
                    //  }
                },
                login: function (type) {
                    if (type === "FACEBOOK"){
                        facebookAuthenticator.login();
                    }
                }


            };
        }]);
