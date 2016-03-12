/**
 * Created by yotam on 12/3/2016.
 */
angular.module('app.userDetails')

    .controller('userDetailsCtrl', ['$scope',
        function ($scope) {
            var ctrl = this;
            function _init() {
                $scope.vm = {
                    user :$scope.userData
                };
            };

            $scope.createPhoneNumberObjectIfNotExists = function(){
                if (!$scope.userData.phone_number ){
                    $scope.userData.phone_number = {
                        country_code : 'IL'
                    };
                }
            };
            $scope.updateUser = function(){
                $scope.onUpdate($scope.userData);
            }
            _init();
        }]);