/**
 * Created by yotam on 31/1/2016.
 */

angular.module('app.footer.footer-ctrl', [])

    .controller('footerCtrl', ['$location', '$rootScope', 'AuthService', 'DialogsService',
        function ($location, $rootScope, AuthService, DialogsService) {
            var ctrl = this;
            var _footerDefaults = {
                title: "",
                subTitle: "",
                shouldShowButton: false
            };

            function _init() {
                ctrl.showHowItWorksSection = false;
                ctrl.footerLinks = [
                    {
                        textKey: "views.main.footer.about_us",
                        link: "/about_us",
                        classes: "about-us"
                    },
                    {
                        textKey: "views.main.footer.terms-and-conditions",
                        link: "/terms_and_conditions",
                        classes: "terms-and-conditions"
                    },
                    {
                        textKey: "views.main.footer.how-it-works",
                        link: "/how_it_works",
                        classes: "how-it-works"
                    },
                    {
                        textKey: "views.main.footer.doners",
                        link: "/partners",
                        classes: "donors"
                    },
                    {
                        textKey: "views.main.footer.success_stories",
                        link: "/success",
                        classes: "success"
                    },
                    {
                        textKey: "views.main.footer.contact_us",
                        link: "/contact_us",
                        classes: "contact-us"
                    }
                ];
                ctrl.footerAttributes = angular.copy(_footerDefaults);
                ctrl.howItWorksLinks = [
                    {
                        title: "views.main.footer.how-it-works.variety_of_cases",
                        subtitle: "views.main.footer.how-it-works.variety_of_cases_subtitle",
                        url: "/cases",
                        imageUrl: "\\assets\\img\\how-it-works\\variety-Of-cases-banner.png"
                    },
                    {
                        title: "views.main.footer.how-it-works.your_way",
                        subtitle: "views.main.footer.how-it-works.your_way_subtitle",
                        url: "/cases",
                        imageUrl: "\\assets\\img\\how-it-works\\your-way-banner.png"
                    },
                    {
                        title: "views.main.footer.how-it-works.help_and_change",
                        subtitle: "views.main.footer.how-it-works.help_and_change_subtitle",
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

            ctrl.onfooterButtonClick = function () {
                ctrl.showHowItWorksSection = !ctrl.showHowItWorksSection;
            }

            ctrl.updatefooterContent = function (toState) {
                var newStateProperties = toState.data || {};
                angular.extend(ctrl.footerAttributes,_footerDefaults,newStateProperties.footer || {})
            };

            ctrl.openLoginDialog = function (ev) {
                DialogsService.openDialog({dialog: 'login'});
            };

            ctrl.isSideNavOpen = false;
            ctrl.toggleSideNav = function (){
              ctrl.isSideNavOpen = !ctrl.isSideNavOpen;
            }

      	    $rootScope.$on('$stateChangeSuccess', function (event, toState, toParams, fromState, fromParams) {
      	        ctrl.updatefooterContent(toState);
      	    	ctrl.isSideNavOpen = false;
      	    });

	          _init();
}]);
