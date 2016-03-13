/**
 * Created by yotam on 26/1/2016.
 */
'use strict';

angular.module('app.casesSearch', ['app.services.share'])

    .config(['$stateProvider', function ($stateProvider) {
        $stateProvider.state('casesSearch', {
            url: "/cases",
            templateUrl: 'casesSearch/casesSearch.html',
            controller: 'casesSearchCtrl',
            data: {
                header: {
                    shouldShowButton: true,
                    subTitle: "views.casesSearch.case.header_subtitle",
                    title: "views.casesSearch.case.header_title"
                }
            }
        });
    }])
    .controller('casesSearchCtrl', ['$scope', 'Restangular', '$stateParams', 'DialogsService', 'moment', '$rootScope','FbShare',
        function ($scope, Restangular, $stateParams, DialogsService, moment, $rootScope, FbShare) {

            // --- INNER FUNCTIONS --- //
            // function createCasesArr(){
            //   var arr = [];
            //   for (var i = 1; i < 24; i++) {
            //       arr.push({
            //         title: ' עזרה בהסעה ' + i,
            //         imgSrc: 'assets/img/face1.jpg',
            //         order: i,
            //       });
            //   }
            //
            //   return arr;
            // }
			var sortTypes = [{
				'type': 'newerFirst',
				'title': 'חדש ביותר',
				'sortField': 'due_date', // change to creation_date
				'sortOrder': 'ASCENDING'
			},
			{
				'type': 'olderFirst',
				'title': 'ישן ביותר',
				'sortField': 'due_date', // change to creation_date
				'sortOrder': 'DESCENDING'
			},
			{
				'type': 'urgentFirst',
				'title': 'דחוף ביותר',
				'sortField': 'due_date',
				'sortOrder': 'DESCENDING'
			}];

            function _init() {
                $scope.vm = {
                    cases: [],
					totalCasesCount: 0,
					currentCasesPage: 1,
					casesPerPage: 5,
                    reverse: false,
					sortTypes: sortTypes,
					currentSortType: sortTypes[0]
                };
				
				var vm = $scope.vm;

                var baseCases = Restangular.all('cases');
                updateCasesListByCurrentPage();
				
				baseCases.customGET("", {'count':'yes'}).then(function (result) {
                    vm.totalCasesCount = result.count;
                });

                vm.changeSort = function (isReversed) {
                    vm.reverse = isReversed;
                }
                vm.onPageChange = function(newPageNumber) {
					updateCasesListByCurrentPage();
					
                  // We want to scroll to top of the list here
                }
				
				vm.onSortChange = function(newSortType){
					if (newSortType == vm.currentSortType)
						return;
					
					vm.currentSortType = newSortType;
					updateCasesListByCurrentPage();
				} 
				
				vm.facebookShare = function(_case) {
				   FbShare.shareCase(_case);
                }
				
				function updateCasesListByCurrentPage(){
					baseCases.getList({
						'sort' : "[('" + vm.currentSortType.sortField + "','" +  vm.currentSortType.sortOrder + "')]",
						'page_size': vm.casesPerPage, 
						'page_number': vm.currentCasesPage - 1 
					}).then(function (cases) {
						vm.cases = cases;
					});
				}
            }

            // --- INIT --- //
            _init();
        }
    ]);
