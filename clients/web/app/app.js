'use strict';

// Declare app level module which depends on views, and components
angular.module('app', [
        // External modules
        'ngRoute',
        'ngMaterial',
        'ngCookies',
        'pascalprecht.translate',// angular-translate
        'restangular',
        'ui.router',

        // App views
        'app.view1',
        'app.view2',
        'app.caseDetail',

        // Components
        'app.version',

        // Services
        'app.services.data-access',
        'app.services.language-service'
    ])
    .constant('LOCALES', {
        'locales': {
            'he_HE': 'עברית',
            'en_US': 'English'
        },
        'preferredLocale': 'he_HE'
    })
    .config(['$urlRouterProvider', '$translateProvider', function ($urlRouterProvider, $translateProvider) {
        // i18n setup based on: https://scotch.io/tutorials/internationalization-of-angularjs-applications
        $translateProvider.useStaticFilesLoader({
            prefix: 'resources/locale-',// path to translations files
            suffix: '.json'// suffix, currently- extension of the translations
        });
        $translateProvider.preferredLanguage('he_HE');// is applied on first load
        $translateProvider.useLocalStorage();// saves selected language to localStorage
        // App routing is using ui-router module - https://github.com/angular-ui/ui-router
        $urlRouterProvider.otherwise("/view1");

    }]);
