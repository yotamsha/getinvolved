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
