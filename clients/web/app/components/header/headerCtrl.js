/**
 * Created by yotam on 31/1/2016.
 */

angular.module('app.header.header-ctrl', [])

    .controller('headerCtrl', ['$location','$rootScope','$scope', function($location, $rootScope, $scope) {
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
        }


/*        $rootScope.header.title = "בואו נתערב"
        $rootScope.header.subTitle = "מגוון אפשרויות להתנדבות חד פעמית שיהפכו רגע פנוי לרגע של שינוי";
        $rootScope.header.shouldShowButton = true;*/
        ctrl.navClass = function (route) {
            var currentRoute = $location.path();
            return route.link === currentRoute ? 'active ' + route.classes : '';
        };

        ctrl.updateHeaderContent = function(toState){
            var newStateProperties = toState.data || {};
            angular.extend(ctrl.headerAttributes,_headerDefaults,newStateProperties.header || {})
        };

        $rootScope.$on('$stateChangeSuccess', function (event, toState, toParams, fromState, fromParams) {
            ctrl.updateHeaderContent(toState);
        });
        _init();
    }]);
