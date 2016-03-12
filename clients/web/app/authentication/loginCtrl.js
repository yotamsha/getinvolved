/**
 * Created by yotam on 28/1/2016.
 */
'use strict';

angular.module('app.login', [])

    .controller('loginCtrl', ['$scope', '$mdDialog','AuthService','$timeout','AUTH_EVENTS',
        'data','AUTH_CONTEXTS','UserDao','$rootScope',
        function ($scope, $mdDialog, AuthService, $timeout, AUTH_EVENTS,
                  data, AUTH_CONTEXTS, UserDao, $rootScope) {

            // --- INNER FUNCTIONS --- //

            function _init() {
                console.log("auth popup context: " ,data.context);

                $scope.vm = {
                    user : data.userSession,
                    context : data.context,
                    missingFields : data.missingFields,
                    popupTitle : "views.login.title"

            };
                $scope.AUTH_CONTEXTS = AUTH_CONTEXTS;
                switch (data.context){
                    case AUTH_CONTEXTS.HEADER_LOGIN:
                        break;
                    case AUTH_CONTEXTS.CASE_CREATION:break;
                    case AUTH_CONTEXTS.TASK_ASSIGNMENT:
                        break;
                    case AUTH_CONTEXTS.TASK_ASSIGNMENT_WITH_SESSION:
                        if ($scope.vm.missingFields){
                            $scope.vm.popupTitle = "views.login.completeDetails";
                        } else {
                            $scope.vm.popupTitle = "views.login.verifyDetails";
                        }
                        break;
                }
                $timeout(function(){
                    FB.XFBML.parse();
                },0);
                $scope.$on(AUTH_EVENTS.authenticationCompleted,function(){
                    $scope.hide();
                })
            }

            // --- SCOPE FUNCTIONS --- //

            $scope.hide = function() {
                $mdDialog.hide();
            };
            $scope.cancel = function() {
                $mdDialog.cancel();
            };
            $scope.answer = function(answer) {
                $mdDialog.hide(answer);
            };
            $scope.fbLogin = function(){
                AuthService.login("FACEBOOK");
            };
            $scope.login = function(){
                AuthService.login("REGULAR", $scope.vm.user);
            };
            $scope.updateUser = function(user){
                // if update was successful, then according to the context, requested action should take place.
                UserDao.customPUT(user, user.id).then(function(){
                    // success
                    switch ($scope.vm.context){
                        case AUTH_CONTEXTS.TASK_ASSIGNMENT_WITH_SESSION:
                            $rootScope.$broadcast(AUTH_EVENTS.volunteerDetailsCompleted);
                            $mdDialog.hide();
                            break;
                        case AUTH_CONTEXTS.CASE_CREATION: break;
                    }
                }, function(){
                    // error
                });
                console.log("updating user.." , user);
            };
            // --- INIT --- //

            _init();
        }

    ])
/*    .directive('btFbParse', function () {
        return {
            restrict:'A',
            link:function (scope, element, attrs) {
                console.log(scope.shareurl);//it works
                if(scope.facebookIsReady){
                    FB.XFBML.parse();
                }
            }
        };
    })*/
