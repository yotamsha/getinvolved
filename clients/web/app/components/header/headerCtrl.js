/**
 * Created by yotam on 31/1/2016.
 */

angular.module('app.header.header-ctrl', [])

    .controller('headerCtrl', ['$location', '$rootScope', 'AuthService', 'DialogsService','$filter','AUTH_CONTEXTS',
        function ($location, $rootScope, AuthService, DialogsService, $filter, AUTH_CONTEXTS) {
            var ctrl = this;
            var _headerDefaults = {
                title: "",
                subTitle: "",
                shouldShowButton: false
            };

            function _init() {
                ctrl.showHowItWorksSection = false;
                var logoutRoute = {
                    routeText : "views.main.header.logout",
                    clickHandler : function(){
                        ctrl.authSrv.logout();
                    },
                    showAsPrimaryLinkInMobileOnly : true,
                    hide : function(){
                        return !ctrl.authModel.isAuthenticated;
                    }
                };
                ctrl.headerLinks = [
                    {
                        routeText: "views.main.header.login_or_signup",
                        classes: "login",
                        clickHandler :  ctrl.openLoginDialog,
                        hide : function(){
                            return ctrl.authModel.isAuthenticated || ctrl.authModel.isLoading;
                        }
                    },
                    {
                        routeText: function(){
                            if (ctrl.authModel.userSession){
                                return $filter('translate')('views.main.header.hello') + " " +
                                    ctrl.authModel.userSession.first_name;
                            }
                            return "";
                        },
                        classes: "profile",
                        link: "/profile",
                        isMenu : true,
                        hide : function(){
                            return !ctrl.authModel.isAuthenticated;
                        },
                        menuItems : [ // relevant only for desktop
                            {
                                routeText : "views.main.header.profile",
                                clickHandler : function(){
                                    ctrl.changeRoute('profile')
                                }
                            },
                            logoutRoute
                        ]
                    },
                    {
                        routeText: "views.main.header.nav-menu.opportunities",
                        link: "/cases",
                        classes: "cases"
                    },
                    {
                        routeText: "views.main.header.nav-menu.about_us",
                        link: "/about",
                        classes: "about-us"
                    },
                    {
                        routeText: "views.main.header.nav-menu.donors",
                        link: "/partners",
                        classes: "donors"
                    },
                    {
                        routeText: "views.main.header.nav-menu.success_stories",
                        link: "/success-stories",
                        classes: "success-stories"
                    },
                    {
                        routeText: "views.main.header.nav-menu.contact_us",
                        link: "/contact",
                        classes: "contact"
                    },
                    {
                        routeText: "views.main.header.nav-menu.ask_help",
                        link: "/ask-help",
                        classes: "ask-help"
                    },
                    logoutRoute

                ];

                ctrl.headerAttributes = angular.copy(_headerDefaults);
                ctrl.howItWorksLinks = [
                    {
                        title: "views.main.header.how-it-works.variety_of_cases",
                        subtitle: "views.main.header.how-it-works.variety_of_cases_subtitle",
                        url: "/cases",
                        imageUrl: "\\assets\\img\\how-it-works\\variety-of-cases-banner.png"
                    },
                    {
                        title: "views.main.header.how-it-works.your_way",
                        subtitle: "views.main.header.how-it-works.your_way_subtitle",
                        url: "/cases",
                        imageUrl: "\\assets\\img\\how-it-works\\your-way-banner.png"
                    },
                    {
                        title: "views.main.header.how-it-works.help_and_change",
                        subtitle: "views.main.header.how-it-works.help_and_change_subtitle",
                        url: "/cases",
                        imageUrl: "\\assets\\img\\how-it-works\\help-and-change-banner.png"
                    }
                ];
                ctrl.authSrv = AuthService;
                ctrl.authModel = AuthService.model();
            }

            ctrl.navClass = function (route) {
                var currentRoute = $location.path();
                return route.link === currentRoute ? 'active ' + route.classes : route.classes;
            };

            ctrl.onHeaderButtonClick = function () {
                ctrl.showHowItWorksSection = !ctrl.showHowItWorksSection;
            }

            ctrl.updateHeaderContent = function (toState) {
                var newStateProperties = toState.data || {};
                angular.extend(ctrl.headerAttributes,_headerDefaults,newStateProperties.header || {})
            };

            ctrl.openLoginDialog = function () {
                DialogsService.openDialog({dialog: 'login',locals : {
                    data : {
                        context : AUTH_CONTEXTS.HEADER_LOGIN
                    }
                }});
            };
            ctrl.changeRoute = function(route){
                $location.path(route)
            };
            ctrl.handleMenuClick = function(route){
                if (route.link){
                    $location.path(route.link);
                    return;
                }
                if (route.clickHandler){
                    route.clickHandler();
                }
            };
            ctrl.getRouteText = function(route){
                if (_.isString(route.routeText)){
                    return $filter('translate')(route.routeText);
                } else {
                    return route.routeText();
                }
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
