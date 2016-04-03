'use strict';

angular.module('app.views.helpRequestForm', ['app.vendors.momentjs'])

    .constant('FORM', {
        "DRIVE": "drive",
        "PRODUCT": "product",
        "ACTIVITY": "activity",
        "PROFESSION": "profession",
        "MAINTENANCE": "maintenance",
        "OTHER": "other",
        "NONE": "none"
    })

    .config(['$stateProvider', function($stateProvider) {
            $stateProvider.state('helpRequestForm', {
                url : "/ask-help",
                templateUrl: 'views/ask-help/askHelp.html',
                controller: 'askHelpCtrl',
                controllerAs: "vm"
            });
    }])

    .run(['moment','$mdDateLocale',
        function(moment, $mdDateLocale){
            $mdDateLocale.months = [
                'ינואר',
                'פברואר',
                'מרץ',
                'אפריל',
                'מאי',
                'יוני',
                'יולי',
                'אוגוסט',
                'ספטמבר',
                'אוקטובר',
                'נובמבר',
                'דצמבר'
            ];

            $mdDateLocale.shortMonths = [
                'ינו׳',
                'פבר׳',
                'מרץ',
                'אפר׳',
                'מאי',
                'יוני',
                'יולי',
                'אוג׳',
                'ספט׳',
                'אוק׳',
                'נוב׳',
                'דצ׳'
            ];
            $mdDateLocale.days = [
                'ראשון',
                'שני',
                'שלישי',
                'רביעי',
                'חמישי',
                'שישי',
                'שבת'
            ];
            $mdDateLocale.shortDays = ['א', 'ב', 'ג', 'ד', 'ה', 'ו', 'ש'];
            // Can change week display to start on Monday.
            $mdDateLocale.firstDayOfWeek = 0;
            // Optional.
            //$mdDateLocale.dates = [1, 2, 3, 4, 5, 6];
            // Example uses moment.js to parse and format dates.
            $mdDateLocale.parseDate = function(dateString) {
                var m = moment(dateString, 'L', true);
                return m.isValid() ? m.toDate() : new Date(NaN);
            };
            $mdDateLocale.formatDate = function(date) {
                return moment(date).format('L');
            };
            $mdDateLocale.monthHeaderFormatter = function(date) {
                return $mdDateLocale.months[date.getMonth()] + ' ' + date.getFullYear();
            };
            // In addition to date display, date components also need localized messages
            // for aria-labels for screen-reader users.
            $mdDateLocale.weekNumberFormatter = function(weekNumber) {
                return 'שבוע ' + weekNumber;
            };
            $mdDateLocale.msgCalendar = 'לוח שנה';
            $mdDateLocale.msgOpenCalendar = 'פתח את לוח השנה';
    }])

    .controller('askHelpCtrl', ['$scope', '$http', 'FORM', '$anchorScroll', '$location',
        function ($scope, $http, FORM, $anchorScroll, $location) {
            var vm = this;

            vm.FORM = FORM;
            vm.currForm = "none";
            vm.oneDaySeconds = 60 * 60 * 24; // todo: this will also be fetched from server

            /* this is temporary. todo: create a module that fetches the validations from server */
            vm.valids = {
                task: {
                    description: {
                        length: {
                            min: 10,
                            max: 300 // todo: currently not corresponding with server constraints
                        }
                    },
                    durationMinutes: {
                        length: {
                            min: 60,
                            max: 60 * 24
                        }
                    },
                    dueDate: {
                        hours: {
                            max: 24 // conflicts with dueDate.seconds.max
                        },
                        seconds: {
                            min: vm.oneDaySeconds,
                            max: vm.oneDaySeconds * 90 // conflicts with dueDate.hours.max
                        }
                    }
                },
                facebook: {
                    id: {
                        length: {
                            min: 8,
                            max: 40
                        }
                    },
                    token: {
                        length: {
                            min: 10
                        }
                    }
                }
            };

            vm.img = {
                drive: "/assets/img/ask-help/escort.drive.png",
                product: "/assets/img/ask-help/product.donation.png",
                activity: "/assets/img/ask-help/workshop.activity.png",
                occupation: "/assets/img/ask-help/occupation.oriented.png",
                maintenance: "/assets/img/ask-help/light.maintenance.png",
                other: "/assets/img/ask-help/other.png"
            };

            vm.translatePath = 'views.askHelp';

            // todo: adjust these
            vm.periods = [
                'views.askHelp.hr1',
                'views.askHelp.hr2',
                'views.askHelp.hr3',
                'views.askHelp.hr4-8',
                'views.askHelp.dy0.5',
                'views.askHelp.dy1'
            ];

            vm.hours = [];
            for(var i = 0; i <= 23 ; ++i) {
                vm.hours.push(i);
            }

            vm.minutes = [];
            for(var i = 0; i <= 60 ; ++i) {
                vm.minutes.push(i);
            }

            vm.phoneRegex = /^(\d{8})?(\d{10})?$/; // todo: use a standard way of phone number validation

            //{
            //    'title': "????",
            //    'description': "????",
            //    'petitioner_id': "????", // MongoDB ID
            //    'tasks': [
            //    // Atleast one
            //<task_object/s>
            //],
            //    'state': <optional: string>, // This shouldnt be updated manually, only by ADMINs
            //    'location': <optional: location_object>
            //}

            vm.selectForm = function(selectedForm) {
                // this function is called by ng-click of an image (when user chooses the type of help)
                vm.currForm = selectedForm;
                $location.hash("requestForm");
                $anchorScroll();
            };

            // todo: connect with server
            vm.sendRequest = function() {
                //alert('todo :) send request to server.');
                var req = {
                    method: 'POST',
                    url: 'http://localhost:5000/api/cases',
                    headers: {
                        'access-token': srvAuth.user.token,
                        'me': srvAuth.user.id
                    },
                    data: {
                        'title': 'baryakir',
                        'description' : 'this works. good joooobbbb.',
                        'petitioner_id': '????????',
                        'tasks': [
                            {
                                'volunteer_id': "????", // MongoDB ID,
                                'description': "????",
                                'title': "????",
                                'type': "????",
                                'due_date': "int" // Value in seconds
                                //'state': <optional: string>, // Should not be specified on creation
                                //'id': <optional: string>, // DO NOT specify this on creation, but REQUIRED for updates
                                //'location': <optional: location_object>, // Required for type: transportation
                                //'destination': <optional: location_object> // Required for type: transportation
                            }
                        ]
                    }
                };

                $http(req)
                    .then(function(response) {
                        $scope.postSuccessMsg = "Your card was posted to your friend\'s wall!";
                        alert('posted!')
                        console.log($scope.postSuccessMsg);
                        $scope.postBtnEnabled = true;
                    })
                    .catch(function() {
                        //alert('An error occured. Your card was not posted to Facebook.');
                        $scope.postBtnEnabled = true;
                    });


            };
        }
    ])

    .filter('numberFixedLen', function () {
        return function (n, len) {
            var num = parseInt(n, 10);
            len = parseInt(len, 10);
            if (isNaN(num) || isNaN(len)) {
                return n;
            }
            num = '' + num;
            while (num.length < len) {
                num = '0'+num;
            }
            return num;
        };
    });
