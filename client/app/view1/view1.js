'use strict';

angular.module('myApp.view1', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/view1', {
            templateUrl: 'view1/view1.html',
            controller: 'View1Ctrl'
        });
    }])

    .controller('View1Ctrl', ['$scope', '$http', '$timeout', 'appData', '$q',
        function ($scope, $http, $timeout, appData, $q) {

            // --- INNER FUNCTIONS --- //

            function _init() {
                $scope.vm = {
                    viewData : [1,2,3],
                    tasks : []
                };
            }

            // --- SCOPE FUNCTIONS --- //

            $scope.getModels = function () {

                appData.getAll("tasks")
                    .success(function(data){
                    $scope.vm.dbData = data;
                })
            };
            $scope.saveOrUpdateModel = function () {

                appData.saveOrUpdate("dataModel")
                    .success(function (result) {

                });
            };

            // --- INIT --- //

            _init();
        }

    ]);