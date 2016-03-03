/**
 * Created by yotam on 26/1/2016.
 */
'use strict';

angular.module('app.userProfile', [])

    .config(['$stateProvider', function ($stateProvider) {
        $stateProvider.state('userProfile', {
            url: "/profile",
            templateUrl: 'userProfile/userProfile.html',
            controller: 'userProfileCtrl',
            resolve: { // complete the following requests before page is loaded.
                userSession: ['AuthService', function (AuthService) { // verify that session retrieval is completed.
                    return AuthService.authRetrievalCompleted();
                }]
            }
        });
    }])

    .controller('userProfileCtrl', ['$scope', 'Restangular', '$stateParams', 'AuthService','UserDao',
        function ($scope, Restangular, $stateParams, AuthService, UserDao) {
            // --- INNER VARIABLES --- //

            var _authModel = AuthService.model();

            // --- INNER FUNCTIONS --- //

            function _init() {
                $scope.vm = {};
                $scope.vm.user = angular.copy(_authModel.userSession);
            }

            // --- SCOPE FUNCTIONS --- //
            $scope.createPhoneNumberObjectIfNotExists = function(){
                if (!$scope.vm.user.phone_number){
                    $scope.vm.user.phone_number = {
                        country_code : 'IL'
                    };
                }
            };
            $scope.updateUser = function(){
                UserDao.customPUT($scope.vm.user, $scope.vm.user.id);
            };
            // --- INIT --- //

            _init();
        }

    ]);
