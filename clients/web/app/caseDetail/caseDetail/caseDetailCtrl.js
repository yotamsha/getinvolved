/**
 * Created by yotam on 26/1/2016.
 */
'use strict';

angular.module('app.caseDetail', [])

    .config(['$stateProvider', function ($stateProvider) {
        $stateProvider.state('caseDetail', {
            url: "/case/:caseId",
            templateUrl: 'caseDetail/caseDetail.html',
            controller: 'caseDetailCtrl'
        });
    }])

    .controller('caseDetailCtrl', ['$scope', 'Restangular', '$stateParams','DialogsService','moment',
        function ($scope, Restangular, $stateParams, DialogsService, moment) {

            //var caseDao = Restangular.all('cases');

            // --- INNER FUNCTIONS --- //

            function _init() {
                $scope.vm = {
                    case: {
                        title: "כותרת של המקרה..",
                        description: "טקסט מגניב בעברית שמתאר משהו",
                        imgUrl : "assets/img/face1.jpg",
                        tasks : [
                            {
                                title : "הסעה לבת ים",
                                date : moment().format('LLLL'),
                                location : "תל אביב"
                            },
                            {
                                title : "עזרה בקניות",
                                date : moment().format('LLLL'),
                                location : "תל אביב"
                            },
                            {
                                title : "ניקיון דירה",
                                date : moment().format('LLLL'),
                                location : "תל אביב"
                            }
                        ]
                    }

                };
            }

            // --- SCOPE FUNCTIONS --- //
            $scope.openLoginDialog = function(ev) {
                DialogsService.openDialog({dialog : 'login'});
            };
            // --- INIT --- //

            _init();
        }

    ]);
