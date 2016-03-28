/**
 * Created by yotam on 14/3/2016.
 */
angular.module('app.models.case')
    .factory('CaseMapper', ['CaseDefaultImageProvider','TaskMapper', function (CaseDefaultImageProvider , TaskMapper) {
        
		
        function _mapToVM(caseDto){
            var caseVM = {
				id: caseDto.id, 
				title: caseDto.title,
				description: caseDto.description,
				state: caseDto.state, // should be mapped to CaseState?
				location: caseDto.location,
				tasks: TaskMapper.mapCollectionToVM(caseDto.tasks),		
			};
			
            caseVM.imgUrl = caseDto.imgUrl ? caseDto.imgUrl : CaseDefaultImageProvider.getImage();
			
            return caseVM;
        }
		
		function _mapToDto(caseVm){
            var caseDto = angular.copy(caseVm); // TODO add correct logic here
            
			return caseDto;
        }
		
		function _mapCollectionToVM(list){
            var vmList = _.map(list, _mapToVM);
			
            return vmList;
        }
		
        function _mapCollectionToDtos(list){
            var dtoList = _.map(list, _mapToDto);
            
			return dtoList;
        }
		
        return {
            mapCollectionToDtos : _mapCollectionToDtos,
            mapToDto : _mapToDto,
            mapCollectionToVM : _mapCollectionToVM,
            mapToVM : _mapToVM
        };
    }]);