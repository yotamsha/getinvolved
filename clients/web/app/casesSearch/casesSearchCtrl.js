/**
 * Created by yotam on 26/1/2016.
 */
'use strict';

angular.module('app.casesSearch', [])

    .config(['$stateProvider', function ($stateProvider) {
        $stateProvider.state('casesSearch', {
            url: "/cases",
            templateUrl: 'casesSearch/casesSearch.html',
            controller: 'casesSearchCtrl'
        });
    }])
    .controller('casesSearchCtrl', ['$scope', 'Restangular', '$stateParams','DialogsService','moment','$rootScope',
        function ($scope, Restangular, $stateParams, DialogsService, moment, $rootScope) {
            $rootScope.header.title = "בואו נתערב"
            $rootScope.header.subTitle = "מגוון אפשרויות להתנדבות חד פעמית שיהפכו רגע פנוי לרגע של שינוי";
            $rootScope.header.shouldShowButton = true;
            // --- INNER FUNCTIONS --- //
            // function createCasesArr(){
            //   var arr = [];
            //   for (var i = 1; i < 24; i++) {
            //       arr.push({
            //         title: ' עזרה בהסעה ' + i,
            //         imgSrc: 'assets/img/face1.jpg',
            //         order: i,
            //       });
            //   }
            //
            //   return arr;
            // }

            function _init() {
                $scope.vm = {
                  cases : [],
                  reverse: false
                };

                var baseCases = Restangular.all('cases');
                baseCases.getList().then(function(cases){
                  $scope.vm.cases = cases;
                });

                $scope.vm.changeSort = function(isReversed){
                    $scope.vm.reverse = isReversed;
                }
            }

            // --- INIT --- //

            _init();
        }

    ]);
