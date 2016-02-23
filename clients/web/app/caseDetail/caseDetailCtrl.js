/**
 * Created by yotam on 26/1/2016.
 */
'use strict';

angular.module('app.caseDetail', [])

    .config(['$stateProvider', function ($stateProvider) {
        $stateProvider.state('caseDetail', {
            url: "/case/:caseId",
            templateUrl: 'caseDetail/caseDetail.html',
            controller: 'caseDetailCtrl',
            resolve: { // complete the following requests before page is loaded.
                caseData: ['CaseDao', '$stateParams', function (CaseDao, $stateParams) {
                    return CaseDao.get($stateParams.caseId); // load the case data.
                }],
                userSession : ['AuthService', function(AuthService){ // verify that session retrieval is completed.
                    return AuthService.authRetrievalCompleted();
                }]
            }
        });
    }])

    .controller('caseDetailCtrl', ['$scope', 'Restangular', '$stateParams', 'DialogsService', 'moment', 'CaseDao', 'caseData','AuthService',
        function ($scope, Restangular, $stateParams, DialogsService, moment, CaseDao, caseData, AuthService) {

            // --- INNER VARIABLES --- //

            var _authModel = AuthService.model();
            //console.log( Restangular.all('cases'));

            // --- INNER FUNCTIONS --- //
            function caseLoaded(caseData) {
                $scope.vm.case = caseData;

            }

            function _init() {
                $scope.vm = {
                    /*    case: {
                     title: "כותרת של המקרה..",
                     description: "טקסט מגניב בעברית שמתאר משהו",
                     imgUrl : "assets/img/face1.jpg",
                     tasks : [
                     {
                     title : "הסעה לבת ים",
                     date : moment().format('LLLL'),
                     location : "תל אביב"
                     },
                     {
                     title : "עזרה בקניות",
                     date : moment().format('LLLL'),
                     location : "תל אביב"
                     },
                     {
                     title : "ניקיון דירה",
                     date : moment().format('LLLL'),
                     location : "תל אביב"
                     }
                     ]
                     }*/

                };
                $scope.vm.case = caseData;
                console.log( $scope.vm.case);

                /*                $scope.$on(AUTH_EVENTS.authenticationCompleted,function(user){
                                    console.log("caseDetailCtrl: user session loaded", JSON.stringify(user));
                                });*/

            }
            function _taskAssignedCb(){
                console.log("task assigned");
            }
            // --- SCOPE FUNCTIONS --- //
            $scope.openLoginDialog = function (ev) {
                DialogsService.openDialog({dialog: 'login'});
            };
            $scope.assignTaskToUser = function (task) {
                if (_authModel.userSession) { // if user is allowed to be assigned a task
                    $scope.vm.case.assignTaskState(task.id, 'assigned', _authModel.userSession.id).then(_taskAssignedCb,function(){

                    });
                } else {
                    $scope.openLoginDialog();
                }




            }
            // --- INIT --- //

            _init();
        }

    ]);
