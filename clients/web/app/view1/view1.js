'use strict';

angular.module('app.view1', [])

    .config(['$stateProvider', function ($stateProvider) {
        $stateProvider.state('view1', {
            url : "/view1",
            templateUrl: 'view1/view1.html',
            controller: 'View1Ctrl'
        });
    }])

    .controller('View1Ctrl', ['$scope', '$http', '$timeout', 'appData', '$q','$filter','Restangular',
        function View1Ctrl($scope, $http, $timeout, appData, $q, $filter, Restangular) {

            var tasksDao = Restangular.all('tasks');

            // --- INNER FUNCTIONS --- //

            function _init() {
                $scope.vm = {
                    viewData : [1,2,3],
                    dynamicallyTranslatedText : $filter('translate')('dynamic.text')

            };
            }

            // --- SCOPE FUNCTIONS --- //

            $scope.getTasks = function () {

                tasksDao.getList()
                    .then(function(data){
                    $scope.vm.dbData = data;
                });
            };
            $scope.createTask = function () {
                var task = {
                    name : "newTask",
                    description : "bla bla.."
                };
                tasksDao.post(task)
                    .then(function (result) {
                });
            };

            // --- INIT --- //

            _init();
        }

    ]);