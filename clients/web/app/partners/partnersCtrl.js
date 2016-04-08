/**
 * Created by yotam on 26/1/2016.
 */
'use strict';

angular.module('app.partners', [])

    .config(['$stateProvider', function ($stateProvider) {
        $stateProvider.state('partners', {
            url: "/partners",
            templateUrl: 'partners/partners.html',
            controller: 'partnersCtrl'
        });
    }])
    .controller('partnersCtrl', ['$scope', 'Restangular', '$stateParams', 'DialogsService', 'moment', '$rootScope',
        function ($scope, Restangular, $stateParams, DialogsService, moment, $rootScope) {

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
                    partners: [
                        {
                            imgSrc: "/assets/img/partners_logos/250px-Deloitte.svg.png"
                        },
                        {
                            imgSrc: "/assets/img/partners_logos/8200-social.png"
                        },
                        {
                            imgSrc: "/assets/img/partners_logos/bigmazhe_logo_09.04.2013.jpg"
                        },
                        {
                            imgSrc: "/assets/img/partners_logos/endemol-logo.png"
                        },
                        {
                            imgSrc: "/assets/img/partners_logos/ktim.jpg"
                        },
                        {
                            imgSrc: "/assets/img/partners_logos/main-logo.jpg"
                        },
                        {
                            imgSrc: "/assets/img/partners_logos/mccann-logo.png"
                        },
                        {
                            imgSrc: "/assets/img/partners_logos/startop.png"
                        },
                        {
                            imgSrc: "/assets/img/partners_logos/wix_com.png"
                        }
                    ]
                };
            }

            // --- INIT --- //

            _init();
        }

    ]);
