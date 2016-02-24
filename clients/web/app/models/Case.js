/**
 * Created by yotam on 20/2/2016.
 */
/**
 * Model structure inspired by:
 * http://blog.shinetech.com/2014/02/04/rich-object-models-and-angular-js/
 */
angular.module('app.models.case', [])
    /**
     * This is a model wrapper that includes the business logic for a Case.
     */
    .factory('Case', [function () {
        return {
            someCaseLogic: function () {
                return "Some business logic stuff.";
            }
        };
    }])
    /**
     * This factory exposes a data access object for a Case:
     * expose REST methods of Restangular.
     * Possible responsibilities:
     * Parse data before it is sent to server.
     * Parse data before it is presented to client.
     * Caching - if will be needed.
     * Define validations before save.
     */
    .factory('CaseDao', ['Restangular', 'Case', function (Restangular, Case) {

        Restangular.extendModel('cases', function (obj) { // extend the Restangular functionality with the model.
            return angular.extend(obj, Case);
        });

        return Restangular.all('cases');
    }]);