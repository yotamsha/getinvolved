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

    .controller('caseDetailCtrl', ['$scope', 'Restangular', '$stateParams',
        function ($scope, Restangular, $stateParams) {

            var caseDao = Restangular.all('cases');

            // --- INNER FUNCTIONS --- //

            function _init() {
                $scope.vm = {
                    case: {
                        title: "כותרת של המקרה..",
                        description: "טקסט מגניב בעברית שמתאר משהו",
                        imgUrl : "assets/img/face1.jpg"
                    }

                };
            }

            // --- SCOPE FUNCTIONS --- //

            // --- INIT --- //

            _init();
        }

    ]);