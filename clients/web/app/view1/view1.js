'use strict';

angular.module('app.view1', [])

    .config(['$stateProvider', 'USER_ROLES', function ($stateProvider, USER_ROLES) {
        $stateProvider.state('view1', {
            url: "/view1",
            templateUrl: 'view1/view1.html',
            controller: 'View1Ctrl',
/*            resolve: {
                authorize: ['AuthService', function (AuthService) {
                    return AuthService.isAuthorized(USER_ROLES.user);
                }],
            }*/
        });
    }])

    .controller('View1Ctrl', ['$scope', '$http', '$timeout', '$q', '$filter', 'CaseDao',
        function View1Ctrl($scope, $http, $timeout, $q, $filter, CaseDao) {


            // --- INNER FUNCTIONS --- //

            function _init() {
                $scope.vm = {
                    viewData: [1, 2, 3],
                    dynamicallyTranslatedText: $filter('translate')('dynamic.text')

                };
            }

            // --- SCOPE FUNCTIONS --- //

            $scope.getCases = function () {

                CaseDao.getList()
                    .then(function (data) {
                        $scope.vm.dbData = data;
                    });
            };
            $scope.createCase = function () {
                var newCase = {
                    name: "newTask",
                    description: "bla bla.."
                };
                CaseDao.post(newCase)
                    .then(function (result) {
                    });
            };

            // --- INIT --- //

            _init();
        }

    ]);