/**
 * Created by yotam on 31/1/2016.
 */
'use strict';

angular.module('app.footer.footer-directive', [])

    .directive('footer', [ function() {
        return {
            scope: {},
            controller: 'footerCtrl',
            controllerAs: 'ctrl',
            templateUrl: 'components/footer/footer.html'
        };
    }]);
