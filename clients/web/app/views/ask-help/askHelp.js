'use strict';

angular.module('app.views.helpRequestForm', [])

    .config(['$stateProvider', function($stateProvider) {
        $stateProvider.state('helpRequestForm', {
            url : "/help-request",
            templateUrl: 'views/ask-help/askHelp.html',
            controller: 'helpRequestFormCtrl'
        });
    }])

    .controller('helpRequestFormCtrl', ['$scope',
        function ($scope) {

        }
    ]);