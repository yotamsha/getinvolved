/**
 * Created by yotam on 31/1/2016.
 */

angular.module('app.header.header-ctrl', [])

    .controller('headerCtrl', ['$location','$rootScope','AuthService','DialogsService',
        function($location, $rootScope, AuthService, DialogsService) {
        var ctrl = this;
        var _headerDefaults = {
            title : "",
            subTitle : "",
            shouldShowButton : false
        };
        function _init(){
            ctrl.headerLinks = [
                {
                    textKey : "views.main.header.ask_help",
                    link : "/cases",
                    classes : "ask-help"
                },
                {
                    textKey : "views.main.header.login_or_signup",
                    link : "/case/1",
                    classes : "login-signup"
                },
                {
                    textKey : "views.main.header.about_us",
                    link : "/about_us",
                    classes : "about-us"
                }
            ];
            ctrl.headerAttributes = angular.copy(_headerDefaults);

            ctrl.authSrv = AuthService;
            ctrl.authModel = AuthService.model();
        }

        ctrl.navClass = function (route) {
            var currentRoute = $location.path();
            return route.link === currentRoute ? 'active ' + route.classes : '';
        };

        ctrl.updateHeaderContent = function(toState){
            var newStateProperties = toState.data || {};
            angular.extend(ctrl.headerAttributes,_headerDefaults,newStateProperties.header || {})
        };
        ctrl.openLoginDialog = function(ev) {
            DialogsService.openDialog({dialog : 'login'});
        };

        $rootScope.$on('$stateChangeSuccess', function (event, toState, toParams, fromState, fromParams) {
            ctrl.updateHeaderContent(toState);
        });
        _init();
    }]);
