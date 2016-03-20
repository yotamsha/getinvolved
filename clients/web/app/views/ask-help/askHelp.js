'use strict';

angular.module('app.views.helpRequestForm', [])

    .config(['$stateProvider', function($stateProvider) {
        $stateProvider.state('helpRequestForm', {
            url : "/ask-help",
            templateUrl: 'views/ask-help/askHelp.html',
            controller: 'askHelpCtrl as vm'
        });
    }])

    .controller('askHelpCtrl', ['$scope',
        function ($scope) {
            var vm = this;

            vm.imgurl = "http://s9.postimg.org/47m1pb81b/vol.png";

            vm.translatePath = 'views.askHelp';
        }
    ]);