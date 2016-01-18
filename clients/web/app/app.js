'use strict';

// Declare app level module which depends on views, and components
angular.module('myApp', [
        // External modules
        'ngRoute',
        'ngMaterial',
        'ngCookies',
        'pascalprecht.translate',// angular-translate
        'restangular',

        // App views
        'myApp.view1',
        'myApp.view2',

        // Components
        'myApp.version',

        // Services
        'myApp.services.data-access',
        'myApp.services.language-service'
    ])
    .constant('LOCALES', {
        'locales': {
            'he_HE': 'עברית',
            'en_US': 'English'
        },
        'preferredLocale': 'he_HE'
    })
    .config(['$routeProvider', '$translateProvider', function ($routeProvider, $translateProvider) {
        // i18n setup based on: https://scotch.io/tutorials/internationalization-of-angularjs-applications
        $translateProvider.useStaticFilesLoader({
            prefix: 'resources/locale-',// path to translations files
            suffix: '.json'// suffix, currently- extension of the translations
        });
        $translateProvider.preferredLanguage('he_HE');// is applied on first load
        $translateProvider.useLocalStorage();// saves selected language to localStorage

        $routeProvider.otherwise({redirectTo: '/view1'});
    }]);
