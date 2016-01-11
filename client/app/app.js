'use strict';

// Declare app level module which depends on views, and components
angular.module('myApp', [
    // External modules
    'ngRoute',
    'ngMaterial',

    // App views
    'myApp.view1',
    'myApp.view2',

    // Components
    'myApp.version',

    // Services
    'myApp.services.data-access'
]).
config(['$routeProvider', function ($routeProvider) {
    $routeProvider.otherwise({redirectTo: '/view1'});
}]);
