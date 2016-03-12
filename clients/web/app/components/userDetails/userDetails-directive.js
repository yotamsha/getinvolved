/**
 * Created by yotam on 31/1/2016.
 */
'use strict';

angular.module('app.userDetails')
    .directive('userDetails', [ function() {
        return {
            restrict : "E",
            controller: 'userDetailsCtrl',
            controllerAs: 'ctrl',
            templateUrl: 'components/userDetails/userDetails.html',
            scope : {
                userData : "=",
                onUpdate : "=",
            },
            link: function(scope, element, attrs){

            }
        };
    }]);
