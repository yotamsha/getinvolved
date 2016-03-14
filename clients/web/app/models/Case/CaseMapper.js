/**
 * Created by yotam on 14/3/2016.
 */
angular.module('app.models.case')
    /**
     * This is a model wrapper that includes the business logic for a Case.
     */
    .factory('CaseMapper', ['CaseModel','moment', function (CaseModel, moment) {
        function _mapCollectionToVM(list){
            var vmList = _.each(list, _mapToVM);
            return vmList;
        }
        function _mapToVM(caseDto){
            // obj.tasks = TaskResponseMapper.mapCollecion();
            var caseVM = angular.copy(caseDto); // TODO add correct logic here
            caseVM.imgUrl = caseVM.imgUrl ? caseVM.imgUrl : CaseModel.chooseDefaultImage();
            _.each(caseVM.tasks,function(task){
                task.due_date_string_format = moment(task.due_date).format('LLLL');

            });
            return caseVM;
        }
        function _mapCollectionToDtos(list){
            var dtoList = _.each(list);
            return dtoList;
        }
        function _mapToDto(caseVm){
            var caseDto = angular.copy(caseVm); // TODO add correct logic here
            return caseDto;
        }

        return {
            mapCollectionToDtos : _mapCollectionToDtos,
            mapToDto : _mapToDto,
            mapCollectionToVM : _mapCollectionToVM,
            mapToVM : _mapToVM
        };
    }])