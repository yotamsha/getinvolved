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
    .config(function(RestangularProvider) {
        RestangularProvider.setBaseUrl('http://localhost:5000/api');
        RestangularProvider.setDefaultHeaders({
           "Authorization": "Basic YWRtaW46YWRtaW4="
         });
    })
    .controller('casesSearchCtrl', ['$scope', 'Restangular', '$stateParams','DialogsService','moment',
        function ($scope, Restangular, $stateParams, DialogsService, moment) {



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
