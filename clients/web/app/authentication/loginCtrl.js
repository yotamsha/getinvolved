/**
 * Created by yotam on 28/1/2016.
 */
'use strict';

angular.module('app.login', [])

    .controller('loginCtrl', ['$scope', '$mdDialog','AuthService','$timeout',
        function ($scope, $mdDialog, AuthService, $timeout) {

            // --- INNER FUNCTIONS --- //

            function _init() {
                $scope.username = "admin";
                $scope.password = "admin";
                $timeout(function(){
                    FB.XFBML.parse();
                },0);
            }

            // --- SCOPE FUNCTIONS --- //

            // reset login status
            AuthService.clearCredentials();

            $scope.login = function () {

                $scope.dataLoading = true;
                AuthService.login($scope.username, $scope.password, function(response) {
                    console.log("login response: " ,response);
                    if(response.success) {
                        AuthService.setCredentials($scope.username, $scope.password);
                        //$location.path('/');
                    } else {
                        $scope.error = response.message;
                        $scope.dataLoading = false;
                    }
                });
            };
            $scope.hide = function() {
                $mdDialog.hide();
            };
            $scope.cancel = function() {
                $mdDialog.cancel();
            };
            $scope.answer = function(answer) {
                $mdDialog.hide(answer);
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
