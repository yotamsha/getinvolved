'use strict';

// Declare app level module which depends on views, and components
angular.module('app', [

        // External modules
        'ngAnimate',
        'angularUtils.directives.dirPagination',
        'ngRoute',
        'ngMaterial',
        'ngCookies',
        'ngSanitize',
        'ngMessages',
        'pascalprecht.translate',// angular-translate
        'restangular',
        'ui.router',

        // common
        'app.common.constants',

        // App views
        'app.views.helpRequestForm',
        'app.caseDetail',
        'app.casesSearch',
        'app.login',
        'app.userProfile',
        'app.partners',
        'app.views.about',
        'app.views.contact',

        // Components
        'app.version',
        'app.header',
        'app.userDetails',
        'app.footer',

        // Models
        'app.models.case',
        'app.models.task',
        'app.models.user',

        // Services
        'app.services.data-access',
        'app.services.language-service',
        'app.services.dialogs-service',
        'app.services.authentication.auth-service',
        'app.services.interceptors',

        // 3rd-Party Wrappers - We wrap 3rd party libraries that aren't angular modules in order
        // to keep the global window clean. Only these libraries are accessible through a single variable: window._thirdParty
        // more on the method: http://jameshill.io/articles/angular-third-party-injection-pattern/
        'app.vendors.momentjs',

        // Environment config module
        'config'

    ])
    .constant('LOCALES', {
        'locales': {
            'he_HE': 'עברית',
            'en_US': 'English'
        },
        'preferredLocale': 'he_HE'
    })
    .constant('APP_CONFIG', {
        homeRoute: '/cases',
        serverPort : 5000,
        productionServerHost : '104.155.49.192'
    })
    .config(['$urlRouterProvider', '$translateProvider', '$mdThemingProvider', 'RestangularProvider', 'APP_CONFIG','ENV', 'LOCALES',
        function ($urlRouterProvider, $translateProvider, $mdThemingProvider, RestangularProvider, APP_CONFIG, ENV, LOCALES) {

            function getEnvFromHost(){
                //TODO change this to be taken out of some parameter set in the grunt release package command.
                if (location.host === APP_CONFIG.productionServerHost){
                    return "production";
                } else {
                    return "dev";
                }
            }

            function getServerHost(env){
                if (env === "production"){
                    return "http://" + APP_CONFIG.productionServerHost + ":" + APP_CONFIG.serverPort;
                } else {
                    return "http://localhost:" + APP_CONFIG.serverPort;
                }
            }

            //var env = getEnvFromHost();
            var serverHost = ENV.apiEndpoint;
            console.log("using server host: " + serverHost)
            RestangularProvider.setBaseUrl(serverHost + '/api');
            APP_CONFIG.serverHost = serverHost;
            $mdThemingProvider.theme('default')
                .primaryPalette('cyan')
                .accentPalette('orange');

            // i18n setup based on: https://scotch.io/tutorials/internationalization-of-angularjs-applications
            $translateProvider.useStaticFilesLoader({
                prefix: 'resources/locale-',// path to translations files
                suffix: '.json'// suffix, currently- extension of the translations
            });
            $translateProvider.preferredLanguage(LOCALES.preferredLocale);// is applied on first load // todo: use LOCALES.preferredLocale
            $translateProvider.useLocalStorage();// saves selected language to localStorage
            // App routing is using ui-router module - https://github.com/angular-ui/ui-router
            $urlRouterProvider.otherwise(APP_CONFIG.homeRoute);

        }])
    .run(['moment', '$http', '$rootScope', 'AuthService', '$window', function (moment, $http, $rootScope, AuthService, $window) {
        // TODO
        // - Get session state, and set it to the stateManager, and to the Authorization header.
        // - Add an event listener that validate that each route that requires authentication or authorization
        // passes the tests.
        facebookInit();
        moment.locale('he');


        function facebookInit() {

            $window.fbAsyncInit = function () {
                // Executed when the SDK is loaded
                FB.init({
                    appId: '836437249818535',
                    cookie: true,  // enable cookies to allow the server to access
                                   // the session
                    xfbml: true,  // parse social plugins on this page
                    version: 'v2.2' // use version 2.2
                });
                //AuthService.facebookAuthenticator.watchAuthenticationStatusChange();

            };
            (function (d, s, id) {
                var js, fjs = d.getElementsByTagName(s)[0];
                if (d.getElementById(id)) return;
                js = d.createElement(s);
                js.id = id;
                js.src = "//connect.facebook.net/en_US/sdk.js";
                fjs.parentNode.insertBefore(js, fjs);
            }(document, 'script', 'facebook-jssdk'));
        }
    }]);
