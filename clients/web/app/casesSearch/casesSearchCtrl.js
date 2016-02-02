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

    .controller('casesSearchCtrl', ['$scope', 'Restangular', '$stateParams','DialogsService','moment',
        function ($scope, Restangular, $stateParams, DialogsService, moment) {

            //var caseDao = Restangular.all('cases');

            // --- INNER FUNCTIONS --- //

            function _init() {
                $scope.vm = {
                  cases : [
                    {
                      title: 'אהלן אחי',
                      imgSrc: 'assets/img/face1.jpg'
                    }
                  ]
                };
            }

            // --- SCOPE FUNCTIONS --- //
            // $scope.openLoginDialog = function(ev) {
            //     DialogsService.openDialog({dialog : 'login'});
            // };
            // --- INIT --- //

            _init();
        }

    ]);
