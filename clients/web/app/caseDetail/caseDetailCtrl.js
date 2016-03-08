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
                caseData: ['CaseDao', '$stateParams','Restangular', function (CaseDao, $stateParams, Restangular) {
                    //return CaseDao.one("",$stateParams.caseId).get({add_volunteer_attributes : "yes"});
                    return Restangular.one('cases', $stateParams.caseId).get({add_volunteer_attributes : "yes"});
                    //return CaseDao.one("",$stateParams.caseId).customGET("", {add_volunteer_attributes : "yes"}); // load the case data.
                }],
                userSession: ['AuthService', function (AuthService) { // verify that session retrieval is completed.
                    return AuthService.authRetrievalCompleted();
                }]
            }
        });
    }])

    .controller('caseDetailCtrl', ['$scope', 'Restangular', '$stateParams', 'DialogsService', 'moment', 'CaseDao', 'caseData', 'AuthService', 'TASK_STATES',
        function ($scope, Restangular, $stateParams, DialogsService, moment, CaseDao, caseData, AuthService, TASK_STATES) {
            // --- INNER VARIABLES --- //

            var _authModel = AuthService.model();
            //console.log( Restangular.all('cases'));

            // --- INNER FUNCTIONS --- //
            function caseLoaded(caseData) {
                $scope.vm.case = caseData;

            }

            function _init() {
                $scope.TASK_STATES = TASK_STATES;
                $scope.vm = {};
                $scope.vm.case = caseData;
                $scope.vm.case.transformToClient();
            }

            function _taskAssignedCb(task) {
                task.state = TASK_STATES.TASK_ASSIGNED;
                task.volunteer_id = _authModel.userSession.id;

                console.log("task assigned");
            }

            // --- SCOPE FUNCTIONS --- //
            $scope.openLoginDialog = function (ev) {
                DialogsService.openDialog({dialog: 'login'});
            };
            $scope.assignTaskToUser = function (task) {
                if (_authModel.userSession) { // if user is allowed to be assigned a task
                    $scope.vm.case.assignTaskState(task, TASK_STATES.TASK_ASSIGNED).then(
                        function () { //success
                            _taskAssignedCb(task);
                        }, function () { //error

                        });
                } else {
                    $scope.openLoginDialog();
                }


            }
            // --- INIT --- //

            _init();
        }

    ]);
