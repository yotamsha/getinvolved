/**
 * Created by yotam on 26/1/2016.
 */
'use strict';

angular.module('app.casesSearch', ['app.services.share','app.models.case.viewModelExpanders'])

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
    .controller('casesSearchCtrl', ['$scope', 'CaseDao','FbShare',
	'$anchorScroll','$location','$timeout','$translate','CaseEmailShareExpander',
        function ($scope, CaseDao, FbShare, 
		$anchorScroll, $location, $timeout, $translate, CaseEmailShareExpander) {

            function _init() {
                $scope.vm = {
                    cases: [],
					totalCasesCount: 0,
					currentCasesPage: 1,
					casesPerPage: 12,
					reverse: false,
					sortTypes: [],
					selectedSortIndex: 0,
					resultsShownFrom: 0,
					resultsShownTo: 0
                };
				
				var vm = $scope.vm;
				
				var currentSortType;
				var sortTypes = [];
				initCasesGrid(currentSortType, sortTypes);

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
					vm.currentCasesPage = 1;
					currentSortType = newSortType;
					updateCasesListByCurrentPage();
				} 
				
				vm.facebookShare = function(_case) {
				   FbShare.shareCase(_case);
                }
				
				function initCasesGrid(){
					$translate(['views.casesSearch.sortTypes.newest','views.casesSearch.sortTypes.oldest', 
					'views.casesSearch.sortTypes.mostUrgent']).then(function (translations) {
						sortTypes = getSortTypes(translations);
						
						vm.sortTypes = sortTypes;
						currentSortType = sortTypes[0];
						updateCasesListByCurrentPage();
					});
				}
				
				function updateCasesListByCurrentPage() {
										
					CaseDao
						.getMany({
							excludedStates: ["completed", "assigned"],
							pageNum: vm.currentCasesPage - 1,
							pageSize: vm.casesPerPage,
							sort: currentSortType.sortMethod
						})
						.then(function (data) {
							vm.totalCasesCount = data.totalCount;
							vm.cases = data.results;
							vm.resultsShownFrom = ((vm.currentCasesPage - 1) * vm.casesPerPage) + 1;
							var resultsShownTo = vm.currentCasesPage * vm.casesPerPage; 
							vm.resultsShownTo = resultsShownTo > vm.totalCasesCount ? vm.totalCasesCount : resultsShownTo;  
							
							CaseEmailShareExpander.expandCases(vm.cases);
						});
				}
				
				function getSortTypes(translations){
					return [{
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
				}
            }

            // --- INIT --- //
            _init();
        }
    ]);
