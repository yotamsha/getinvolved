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
            vm.periods = [
                'views.askHelp.hr1',
                'views.askHelp.hr2',
                'views.askHelp.hr3',
                'views.askHelp.hr4-8',
                'views.askHelp.dy0.5',
                'views.askHelp.dy1',
            ]
        }
    ]);