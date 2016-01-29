/**
 * Created by yotam on 28/1/2016.
 */
'use strict';

angular.module('app.login', [])

    .controller('loginCtrl', ['$scope', '$mdDialog',
        function ($scope, $mdDialog) {

            // --- INNER FUNCTIONS --- //

            function _init() {

            }

            // --- SCOPE FUNCTIONS --- //
            $scope.hide = function() {
                console.log("Hiding Dialog");
                $mdDialog.hide();
            };
            $scope.cancel = function() {
                console.log("Dialog cancelled ");
                $mdDialog.cancel();
            };
            $scope.answer = function(answer) {
                console.log("Dialog answer: " +answer);
                $mdDialog.hide(answer);
            };
            // --- INIT --- //

            _init();
        }

    ]);
