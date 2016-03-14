/**
 * Created by yotam on 14/3/2016.
 */
angular.module('app.models.task')
    /**
     * This is a model wrapper that includes the business logic for a Case.
     */
    .factory('TaskMapper', ['moment', function ( moment) {
        function _mapCollectionToVM(list){
            var vmList = _.each(list, _mapToVM);
            return vmList;
        }
        function _mapToVM(taskDto){
            var taskVM = angular.copy(taskDto); // TODO add correct logic here
            return taskVM;
        }
        function _mapCollectionToDtos(list){
            var dtoList = _.each(list);
            return dtoList;
        }
        function _mapToDto(taskVm){
            var taskDto = angular.copy(taskVm); // TODO add correct logic here
            return taskDto;
        }

        return {
            mapCollectionToDtos : _mapCollectionToDtos,
            mapToDto : _mapToDto,
            mapCollectionToVM : _mapCollectionToVM,
            mapToVM : _mapToVM
        };
    }])