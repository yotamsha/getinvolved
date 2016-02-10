/**
 * Created by yotam on 31/1/2016.
 */
angular.module('app.header.header-ctrl', [])

    .controller('headerCtrl', ['$location', function($location) {
        var ctrl = this;
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
        ctrl.navClass = function (route) {
            var currentRoute = $location.path();
            return route.link === currentRoute ? 'active ' + route.classes : '';
        };
        /*        "views.main.header.login_or_signup" : "כניסה / הרשמה",
                    "views.main.header.ask_help" : "לבקש עזרה",
                    "views.main.header.about_us" : "קצת עלינו",
                    "views.main.header.donors" : "תורמים",
                    "views.main.header.opportunities" : "הזדמנויות",
                    "views.main.header.success_stories" : "הצלחות",
                    "views.main.header.troubleshooting" : "מסתבכים? דברו איתנו",*/
        ctrl.someValue = 3;
    }]);
