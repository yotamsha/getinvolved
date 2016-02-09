/**
 * Created by yotam on 31/1/2016.
 */
angular.module('app.header.header-ctrl', [])

    .controller('headerCtrl', ['$location', function($location) {
        var ctrl = this;
        ctrl.headerLinks = [
            {
                textKey : "views.main.header.ask_help",
                link : "/case/1",
            },
            {
                textKey : "views.main.header.login_or_signup",
                link : "/login",
            },

            {
                textKey : "views.main.header.about_us",
                link : "/cases",
            },
            {
                textKey : "views.main.header.donors",
                link : "/view1",
            },
        ];
        ctrl.navClass = function (page) {
            var currentRoute = $location.path();
            console.log("page: "+page);
            console.log("currentRoute: "+currentRoute);
            console.log("page === currentRoute: "+(page === currentRoute));
            return page === currentRoute ? 'active' : '';
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
