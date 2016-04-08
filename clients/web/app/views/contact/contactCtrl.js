/**
 * Created by yotam on 26/1/2016.
 */
'use strict';

angular.module('app.views.contact', [])

    .config(['$stateProvider', function ($stateProvider) {
        $stateProvider.state('contact', {
            url: "/contact",
            templateUrl: 'views/contact/contact.html',
            controller: 'contactCtrl'
        });
    }])
    .controller('contactCtrl', ['$scope', 'Restangular', '$stateParams', 'DialogsService', 'moment', '$rootScope',
        function ($scope, Restangular, $stateParams, DialogsService, moment, $rootScope) {

            function _init() {
                $scope.vm = {
                    teamMembers: [
                    {
                        imgSrc : "/assets/img/contact_us/image1.jpg",
                        name : "דנה כהן",
                        title: "מייסדת"
                    },
                                     {
                        imgSrc : "/assets/img/contact_us/avishai.jpg",
                        name : "אבישי בלדרמן",
                        title: "CTO"
                    },               {
                        imgSrc : "/assets/img/contact_us/bar.jpg",
                        name : "בר וכטל",
                        title: "Server dev."
                    },               {
                        imgSrc : "/assets/img/contact_us/barak.jpg",
                        name : "ברק אן כהן",
                        title: "יועץ עסקי וארגוני"
                    },               {
                        imgSrc : "/assets/img/contact_us/meir.jpg",
                        name : "מאיר קדוש",
                        title: "מנהל קריאייטיב"
                    },               {
                        imgSrc : "/assets/img/contact_us/merav.jpg",
                        name : "מירב בצר",
                        title: "יועצת פיתוח משאבים"
                    },               {
                        imgSrc : "/assets/img/contact_us/nir.jpg",
                        name : "ניר אינגביר",
                        title: "מנהל מוצר"
                    },               {
                        imgSrc : "/assets/img/contact_us/nivi.jpg",
                        name : "ניבי טפליץ",
                        title: "UX"
                    },               {
                        imgSrc : "/assets/img/contact_us/yoni.jpg",
                        name : "יוני דור",
                        title: "Web dev."
                    },               {
                        imgSrc : "/assets/img/contact_us/yotam.jpg",
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
