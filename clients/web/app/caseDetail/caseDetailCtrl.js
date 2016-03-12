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
                caseData: ['CaseDao', '$stateParams', 'Restangular', function (CaseDao, $stateParams, Restangular) {
                    //return CaseDao.one("",$stateParams.caseId).get({add_volunteer_attributes : "yes"});
                    return Restangular.one('cases', $stateParams.caseId).get({add_volunteer_attributes: "yes"});
                    //return CaseDao.one("",$stateParams.caseId).customGET("", {add_volunteer_attributes : "yes"}); // load the case data.
                }],
                userSession: ['AuthService', function (AuthService) { // verify that session retrieval is completed.
                    return AuthService.authRetrievalCompleted();
                }]
            }
        });
    }])

    .controller('caseDetailCtrl', ['$scope', 'Restangular', '$stateParams', 'DialogsService',
        'moment', 'CaseDao', 'caseData', 'AuthService', 'TASK_STATES', 'AUTH_CONTEXTS', 'USER_ACTIONS','AUTH_EVENTS',
        function ($scope, Restangular, $stateParams, DialogsService,
                  moment, CaseDao, caseData, AuthService, TASK_STATES, AUTH_CONTEXTS, USER_ACTIONS, AUTH_EVENTS) {
            // --- INNER VARIABLES --- //

            var _authModel = AuthService.model();
            var _taskInProgress;
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

                $scope.$on(AUTH_EVENTS.volunteerDetailsCompleted,$scope.volunteerDetailsCompleted);
            }

            function _taskAssignedCb(task) {
                task.state = TASK_STATES.TASK_ASSIGNED;
                task.volunteer_id = _authModel.userSession.id;
                task.volunteer = {
                    first_name : _authModel.userSession.first_name,
                    last_name : _authModel.userSession.last_name
                };
                console.log("task assigned");
            }

            // --- SCOPE FUNCTIONS --- //
            $scope.openLoginDialog = function (context, missingFields) {
                DialogsService.openDialog({
                    dialog: 'login',
                    locals: {
                        data: {
                            context : context,
                            missingFields : missingFields
                        },
                        userSession : _authModel.userSession
                    }
                });
            };
            $scope.assignTaskToUserProcess = function (task) {
                _taskInProgress = task;
                var sessionMissingDataStatus = AuthService.checkForMissingDetails(USER_ACTIONS.TASK_ASSIGNMENT);
                var noSession = sessionMissingDataStatus === "*";
                var partialSession = (sessionMissingDataStatus.length > 0); // some fields are missing.
                if (!noSession && !partialSession) { // if user is allowed to be assigned a task - verify details popup
                    //$scope.assignTaskToUser(task);
                    $scope.openLoginDialog(AUTH_CONTEXTS.TASK_ASSIGNMENT_WITH_SESSION );

                } else {
                    if (noSession) { // no session - login popup (with facebook option only)
                        $scope.openLoginDialog(AUTH_CONTEXTS.TASK_ASSIGNMENT);
                    } else {
                        if (partialSession) { // missing details - complete details popup
                            $scope.openLoginDialog(AUTH_CONTEXTS.TASK_ASSIGNMENT_WITH_SESSION, sessionMissingDataStatus );
                        }
                    }
                }


            };
            $scope.assignTaskToUser = function(task){
                $scope.vm.case.assignTaskState(task, TASK_STATES.TASK_ASSIGNED, _authModel.userSession.id).then(
                    function () { //success
                        _taskAssignedCb(task);
                        _taskInProgress = null;
                    }, function () { //error
                        _taskInProgress = null;
                    });
            };
            $scope.volunteerDetailsCompleted = function(){
                if (_taskInProgress){
                    $scope.assignTaskToUser(_taskInProgress);
                }
            };
            // --- INIT --- //

            _init();
        }

    ]);
