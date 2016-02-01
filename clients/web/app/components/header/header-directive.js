/**
 * Created by yotam on 31/1/2016.
 */
'use strict';

angular.module('app.header.header-directive', [])

    .directive('header', [ function() {
        return {
            scope: {},
            controller: 'headerCtrl',
            controllerAs: 'ctrl',
            templateUrl: 'components/header/header.html'
        };
    }]);
