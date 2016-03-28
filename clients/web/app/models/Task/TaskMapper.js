/**
 * Created by yotam on 14/3/2016.
 */
angular.module('app.models.task')
    .factory('TaskMapper', ['moment', function ( moment) {
        function _mapCollectionToVM(list){
            var vmList = _.map(list, _mapToVM);
			
            return vmList;
        }
        function _mapToVM(taskDto){
            var taskVM = {
				id: taskDto.id,
				volunteer_id: taskDto.volunteer_id,
				title: taskDto.title,
				description: taskDto.description,
				type: taskDto.type,
				due_date: moment(taskDto.due_date).format('LLLL'),
				state: taskDto.state,
				location: taskDto.location,
				destination: taskDto.destination
			}
			
            return taskVM;
        }
        function _mapCollectionToDtos(list) {
            var dtoList = _.map(list);
			
            return dtoList;
        }
		
        function _mapToDto(taskVm){
            var taskDto = angular.copy(taskVm); // TODO reverse mapping
			
            return taskDto;
        }

        return {
            mapCollectionToDtos : _mapCollectionToDtos,
            mapToDto : _mapToDto,
            mapCollectionToVM : _mapCollectionToVM,
            mapToVM : _mapToVM
        };
    }])