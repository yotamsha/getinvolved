/**
 * Created by yotam on 20/2/2016.
 */
/**
 * Model structure inspired by:
 * http://blog.shinetech.com/2014/02/04/rich-object-models-and-angular-js/
 */
angular.module('app.models.user', [])
    /**
     * This is a model wrapper that includes the business logic for a User.
     */
    .factory('User', [function () {
        return {

        };
    }])
    /**
     * This factory exposes a data access object for a User:
     * expose REST methods of Restangular: (https://github.com/mgonto/restangular)
     *    get([queryParams, headers]): Gets the element. Query params and headers are optionals
     *    getList(subElement, [queryParams, headers]): Gets a nested resource. subElement is mandatory. It's a string with the name of the nested resource (and URL). For example buildings
     *    put([queryParams, headers]): Does a put to the current element
     *    post(subElement, elementToPost, [queryParams, headers]): Does a POST and creates a subElement. Subelement is mandatory and is the nested resource. Element to post is the object to post to the server
     *    remove([queryParams, headers]): Does a DELETE. By default, remove sends a request with an empty object, which may cause problems with some servers or browsers. This shows how to configure RESTangular to have no payload.

     * Possible responsibilities:
     * Parse data before it is sent to server.
     * Parse data before it is presented to client.
     * Caching - if will be needed.
     * Define validations before save.
     */
    .factory('UserDao', ['Restangular','User', function (Restangular, User) {

        Restangular.extendModel('users', function (obj) { // extend the Restangular functionality with the model.
            return angular.extend(obj, User, {
                // Perform all transformations before data is saved to server.
                transformForServer : function(){
                    return Restangular.copy(this);
                }
            });
        });
        // It's also possible to extend the collection methods using Restangular.extendCollection().
        return Restangular.all('users');
    }]);