/**
 * Created by yotam on 26/1/2016.
 */
'use strict';

angular.module('app.about_us', [])

    .config(['$stateProvider', function ($stateProvider) {
        $stateProvider.state('about_us', {
            url: "/about",
            templateUrl: 'about_us/about_us.html',
            controller: 'about_usCtrl'
        });
    }])
    .controller('about_usCtrl', ['$scope', 'Restangular', '$stateParams', 'DialogsService', 'moment', '$rootScope',
        function ($scope, Restangular, $stateParams, DialogsService, moment, $rootScope) {

            function _init() {
                $scope.vm = {
                    teamMembers: [
                    {
                        imgSrc : "/assets/img/about_us/image1.jpg",
                        name : "דנה כהן, נועה אורבך",
                        title: "מייסדות"
                    },
                                     {
                        imgSrc : "/assets/img/about_us/avishai.jpg",
                        name : "אבישי בלדרמן",
                        title: "CTO"
                    },               {
                        imgSrc : "/assets/img/about_us/bar.jpg",
                        name : "בר וכטל",
                        title: "Server dev."
                    },               {
                        imgSrc : "/assets/img/about_us/barak.jpg",
                        name : "ברק אן כהן",
                        title: "יועץ עסקי וארגוני"
                    },               {
                        imgSrc : "/assets/img/about_us/meir.jpg",
                        name : "מאיר קדוש",
                        title: "מנהל קריאייטיב"
                    },               {
                        imgSrc : "/assets/img/about_us/merav.jpg",
                        name : "מירב בצר",
                        title: "יועצת פיתוח משאבים"
                    },               {
                        imgSrc : "/assets/img/about_us/nir.jpg",
                        name : "ניר אינגביר",
                        title: "מנהל מוצר"
                    },               {
                        imgSrc : "/assets/img/about_us/nivi.jpg",
                        name : "ניבי טפליץ",
                        title: "UX"
                    },               {
                        imgSrc : "/assets/img/about_us/yoni.jpg",
                        name : "יוני דור",
                        title: "Web dev."
                    },               {
                        imgSrc : "/assets/img/about_us/yotam.jpg",
                        name : "יותם שלו",
                        title: "Web dev."
                    }
                    ]
                };
            }

            // --- INIT --- //

            _init();
        }

    ]);
