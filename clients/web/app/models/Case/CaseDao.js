/**
 * Created by yotam on 14/3/2016.
 */

/**
 * Model structure inspired by:
 * http://blog.shinetech.com/2014/02/04/rich-object-models-and-angular-js/
 */
angular.module('app.models.case')

    /**
     * This factory exposes a data access object for a Case

     * Possible responsibilities:
     * Parse data before it is sent to server.
     * Parse data before it is presented to client.
     * Caching - if will be needed.
     * Define validations before save.
     */
    .factory('CaseDao', ['Restangular','CaseMapper','TaskMapper', function (Restangular, CaseMapper, TaskMapper ) {
        var modelName = 'cases';
        var collectionDAO = Restangular.all(modelName);
        
		function _getById(caseId, config){
            var queryParams = _buildQueryParams(config);
			
            return Restangular
					.one(modelName, caseId)
					.get(queryParams)
					.then(function(response){
						// success
						return CaseMapper.mapToVM(response);
					},function(){
						//error
					});
        }

		function _getMany(config) {
			var conf = angular.extend({
				pageSize: null,
				pageNum: null,
				sort: null,
				excludedStates: [],
			}, config)
			
			var queryParams = _buildQueryParams(conf);
			
			return collectionDAO
					.getList(queryParams)
					.then(function (cases) {
						return _.map(cases, CaseMapper.mapToVM);
					});
		}

		function _getCasesCount(config){
			var conf = angular.extend({
				excludedStates: [],
			}, config)
			
			var queryParams = _buildQueryParams(conf);
			queryParams["count"] = "yes";
			
			return collectionDAO
					.customGET("", queryParams)
					.then(function (result) {
						return result.count;
					});
		}

        function _assignTaskToVolunteer(caseVM, taskVM, userId){
            var caseDto = CaseMapper.mapToDto(caseVM);
            var taskDto = {};
			
            taskDto.id = taskVM.id;
            taskDto.type = taskVM.type;
            taskDto.volunteer_id = userId;
            caseDto.tasks = [taskDto];
            
			return Restangular.one(modelName, caseDto.id).customPUT(caseDto);
        }
        
		function _buildQueryParams(config){
            var params = {};
			
            if (config.populateVolunteer)
                params.add_volunteer_attributes = "yes"
            
			if (config.pageSize)
				params.page_size = config.pageSize;
			
			if (config.pageNum)
				params.page_number = config.pageNum;
			
			if (config.sort)
				params.sort = config.sort;
			
			var filter = _buildFilterQueryParam(config);
			if (filter)
				params.filter = filter;
			
            return params;
        }
		
		function _buildFilterQueryParam(config){
			var filters = [];
			
			if (config.excludedStates && config.excludedStates.length){
				var excludedStatesArr = [];
				var statesFilter = { "$and" : excludedStatesArr };
				
				_.each(config.excludedStates, function(state){
					excludedStatesArr.push({ "state" : { "$ne" : state }})
				});
				
				filters.push(statesFilter);
			}
			
			return filters.length ? { "$and" : filters } : "";
		}
		
		return {
            getById : _getById,
			getMany: _getMany,
			getCasesCount: _getCasesCount,
            assignTaskToVolunteer : _assignTaskToVolunteer
        };
    }]);