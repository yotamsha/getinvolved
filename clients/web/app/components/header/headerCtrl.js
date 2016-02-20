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
          ctrl.showHowItWorksSection = false;
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
        	ctrl.howItWorksLinks = [
            {
                title: "views.main.header.how-it-works.variety_of_cases",
                subtitle: "views.main.header.how-it-works.variety_of_cases_subtitle",
                url : "/cases",
                imageUrl : "\\assets\\img\\how-it-works\\variety-Of-cases-banner.png"
            },
            {
              title: "views.main.header.how-it-works.your_way",
              subtitle: "views.main.header.how-it-works.your_way_subtitle",
              url : "/cases",
              imageUrl : "\\assets\\img\\how-it-works\\your-way-banner.png"
            },
            {
              title: "views.main.header.how-it-works.help_and_change",
              subtitle: "views.main.header.how-it-works.help_and_change_subtitle",
              url : "/cases",
              imageUrl : "\\assets\\img\\how-it-works\\help-and-change-banner.png"
            }
          ];
        }

        ctrl.navClass = function (route) {
            var currentRoute = $location.path();
            return route.link === currentRoute ? 'active ' + route.classes : '';
        };

        ctrl.onHeaderButtonClick = function(){
          ctrl.showHowItWorksSection = !ctrl.showHowItWorksSection;
        }

        ctrl.updateHeaderContent = function(toState){
            var newStateProperties = toState.data || {};
            angular.extend(ctrl.headerAttributes, _headerDefaults, newStateProperties.header || {})
        };
        ctrl.openLoginDialog = function(ev) {
            DialogsService.openDialog({dialog : 'login'});
        };

        ctrl.isSideNavOpen = false;
        ctrl.toggleSideNav = function (){
          ctrl.isSideNavOpen = !ctrl.isSideNavOpen;
        }

        $rootScope.$on('$stateChangeSuccess', function (event, toState, toParams, fromState, fromParams) {
            ctrl.updateHeaderContent(toState);
            ctrl.isSideNavOpen = false;
        });

        _init();
    }]);
