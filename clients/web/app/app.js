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

            RestangularProvider.setBaseUrl('http://localhost:5000/api');
            RestangularProvider.setDefaultHeaders({
                "Authorization": "Basic YWRtaW46YWRtaW4="
            });

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
            $urlRouterProvider.otherwise("/cases");

        }])
    .run(['moment', '$http', '$rootScope', 'AuthService','$window', function (moment, $http, $rootScope, AuthService, $window) {

        function facebookInit(){
            $rootScope.user = {};

            $window.fbAsyncInit = function() {
                // Executed when the SDK is loaded
                FB.init({
                    appId      : '836437249818535',
                    cookie     : true,  // enable cookies to allow the server to access
                                        // the session
                    xfbml      : true,  // parse social plugins on this page
                    version    : 'v2.2' // use version 2.2
                });
                AuthService.facebookAuthenticator.watchAuthenticationStatusChange();

            };
            (function(d, s, id) {
                var js, fjs = d.getElementsByTagName(s)[0];
                if (d.getElementById(id)) return;
                js = d.createElement(s); js.id = id;
                js.src = "//connect.facebook.net/en_US/sdk.js";
                fjs.parentNode.insertBefore(js, fjs);
            }(document, 'script', 'facebook-jssdk'));
        }
        facebookInit();
        moment.locale('he');
    }]);
