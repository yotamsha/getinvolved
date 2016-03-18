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
    .controller('casesSearchCtrl', ['$scope', 'Restangular', '$stateParams', 
	'DialogsService', 'moment', '$rootScope','FbShare','$anchorScroll','$location','$timeout','$translate',
        function ($scope, Restangular, $stateParams,
		 DialogsService, moment, $rootScope, FbShare, $anchorScroll, $location, $timeout, $translate) {

            function _init() {
                $scope.vm = {
                    cases: [],
					totalCasesCount: 0,
					currentCasesPage: 1,
					casesPerPage: 12,
					reverse: false,
					sortTypes: [],
					selectedSortIndex: 0
                };
				
				var vm = $scope.vm;

                var baseCases = Restangular.all('cases');
				
				var currentSortType;
				var sortTypes = [];
				initCasesGrid(currentSortType, sortTypes);
                
				baseCases.customGET("", {'count':'yes'}).then(function (result) {
                    vm.totalCasesCount = result.count;
                });

                vm.changeSort = function (isReversed) {
                    vm.reverse = isReversed;
                }
                vm.onPageChange = function(newPageNumber) {
					updateCasesListByCurrentPage();
					
                  	$timeout(function() {
						$location.hash('your-oppurtunities-title');
						$anchorScroll();
            		});
                }
				
				vm.onSortChange = function(newSortType, sortIndex){
					if (newSortType == currentSortType)
						return;
					
					vm.selectedSortIndex = sortIndex;
					currentSortType = newSortType;
					updateCasesListByCurrentPage();
				} 
				
				vm.facebookShare = function(_case) {
				   FbShare.shareCase(_case);
                }
				
				function initCasesGrid(){
					$translate(['views.casesSearch.sortTypes.newest','views.casesSearch.sortTypes.oldest', 
					'views.casesSearch.sortTypes.mostUrgent']).then(function (translations) {
						sortTypes = [{
							'type': 'newerFirst',
							'title': translations["views.casesSearch.sortTypes.newest"],
							'sortMethod': "[('creation_date','DESCENDING')]"
						},
						{
							'type': 'olderFirst',
							'title': translations["views.casesSearch.sortTypes.oldest"],
							'sortMethod': "[('creation_date','ASCENDING')]"
						},
						{
							'type': 'urgentFirst',
							'title': translations["views.casesSearch.sortTypes.mostUrgent"],
							'sortMethod': "[('due_date','ASCENDING'),('creation_date','DESCENDING')]",
						}];
						
						vm.sortTypes = sortTypes;
						currentSortType = sortTypes[0];
						updateCasesListByCurrentPage();
					});
				}
				
				function updateCasesListByCurrentPage(){
					
					baseCases.getList({
						'sort' : currentSortType.sortMethod,
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
