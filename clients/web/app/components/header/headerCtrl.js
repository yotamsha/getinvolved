/**
 * Created by yotam on 31/1/2016.
 */

angular.module('app.header.header-ctrl', [])

    .controller('headerCtrl', ['$location','$rootScope','$scope', function($location, $rootScope, $scope) {
        var ctrl = this;

        ctrl.title = $rootScope.header.title;
        $scope.$watch(function () { return $rootScope.header.title; }, function (newValue, oldValue) {
          if (newValue !== oldValue)
            ctrl.title = newValue;
        });
        ctrl.subTitle = $rootScope.header.subTitle;
        $scope.$watch(function () { return $rootScope.header.subTitle; }, function (newValue, oldValue) {
          if (newValue !== oldValue)
            ctrl.subTitle = newValue;
        });
        ctrl.shouldShowButton = $rootScope.header.shouldShowButton;
        $scope.$watch(function () { return $rootScope.header.shouldShowButton; }, function (newValue, oldValue) {
          if (newValue !== oldValue)
            ctrl.shouldShowButton = newValue;
        });

        ctrl.showHowItWorksSection = false;
        ctrl.OnHeaderButtonClick = function(){
          ctrl.showHowItWorksSection = !ctrl.showHowItWorksSection;
        }

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

        ctrl.howItWorksLinks = [
            {
                title: "מגוון מקרים",
                subtitle: "בקשות עזרה מכל הארץ ובכל תחום מחכות להתערבות שלך",
                url : "/cases",
                imageUrl : "\\assets\\img\\how-it-works\\variety-Of-cases-banner.png"
            },
            {
              title: "בדרך שלך",
              subtitle: "איפה שנוח לך, מתי שמתאים לך, ולמי שחשוב לך",
              url : "/cases",
              imageUrl : "\\assets\\img\\how-it-works\\your-way-banner.png"
            },
            {
              title: "לעזור ולשנות",
              subtitle: "מתערבים בקטנה, משפיעים בגדול",
              url : "/cases",
              imageUrl : "\\assets\\img\\how-it-works\\help-and-change-banner.png"
            }
        ];

        ctrl.navClass = function (route) {
            var currentRoute = $location.path();
            return route.link === currentRoute ? 'active ' + route.classes : '';
        };
    }]);
