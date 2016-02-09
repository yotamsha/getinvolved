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
        'app.casesSearch',
        'app.login',

        // Components
        'app.version',
        'app.header',

        // Services
        'app.services.data-access',
        'app.services.language-service',
        'app.services.dialogs-service',
        'app.services.authentication.auth-service',

        // 3rd-Party Wrappers - We wrap 3rd party libraries that aren't angular modules in order
        // to keep the global window clean. Only these libraries are accessible through a single variable: window._thirdParty
        // more on the method: http://jameshill.io/articles/angular-third-party-injection-pattern/
        'app.vendors.momentjs'

    ])
    .constant('LOCALES', {
        'locales': {
            'he_HE': 'עברית',
            'en_US': 'English'
        },
        'preferredLocale': 'he_HE'
    })
    .config(['$urlRouterProvider', '$translateProvider', '$mdThemingProvider', 'RestangularProvider','$httpProvider',
        function ($urlRouterProvider, $translateProvider, $mdThemingProvider, RestangularProvider, $httpProvider) {
            RestangularProvider.setBaseUrl('http://127.0.0.1:5000/api');

/*            $httpProvider.defaults.useXDomain = true;
            $httpProvider.defaults.withCredentials = true;
            delete $httpProvider.defaults.headers.common["X-Requested-With"];
            $httpProvider.defaults.headers.common["Accept"] = "application/json";
            $httpProvider.defaults.headers.common["Content-Type"] = "application/json";*/

            $mdThemingProvider.theme('default')
                .primaryPalette('cyan')
                .accentPalette('orange');

            // i18n setup based on: https://scotch.io/tutorials/internationalization-of-angularjs-applications
            $translateProvider.useStaticFilesLoader({
                prefix: 'resources/locale-',// path to translations files
                suffix: '.json'// suffix, currently- extension of the translations
            });
            $translateProvider.preferredLanguage('he_HE');// is applied on first load
            $translateProvider.useLocalStorage();// saves selected language to localStorage
            // App routing is using ui-router module - https://github.com/angular-ui/ui-router
            $urlRouterProvider.otherwise("/view1");

        }])
    .run(['moment', '$http', '$rootScope', '$cookieStore', function (moment, $http, $rootScope, $cookieStore) {
        // keep user logged in after page refresh
        $rootScope.globals = $cookieStore.get('globals') || {};
        if ($rootScope.globals.currentUser) {
            $http.defaults.headers.common['Authorization'] = 'Basic ' + $rootScope.globals.currentUser.authdata; // jshint ignore:line
        }

        moment.locale('he');
    }])
