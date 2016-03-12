/**
 * Created by yotam on 28/1/2016.
 */
'use strict';

angular.module('app.login', [])

    .controller('loginCtrl', ['$scope', '$mdDialog','AuthService','$timeout','AUTH_EVENTS',
        function ($scope, $mdDialog, AuthService, $timeout, AUTH_EVENTS) {

            // --- INNER FUNCTIONS --- //

            function _init() {
                $scope.vm = {
                    user : {

                    }
                };
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
