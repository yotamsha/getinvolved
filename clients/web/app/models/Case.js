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
            populateWithUsersData : function(users){
                _.each(this.tasks, function(task){
                    var volunteer = _.findWhere(users,{id : task.volunteer_id});
                    if (volunteer){
                        task.volunteer_name = volunteer.first_name + " " + volunteer.last_name;
                    }
                });

            }
        };
    }])
    /**
     * This factory exposes a data access object for a Case:
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
    .factory('CaseDao', ['Restangular','Case','TASK_STATES', function (Restangular, Case, TASK_STATES) {

        Restangular.extendModel('cases', function (obj) { // extend the Restangular functionality with the model.
            return angular.extend(obj, Case, {
                // Perform all transformations before data is saved to server.
                //TODO some of this functionality should be in a Base class.
                // TODO use a helper function that filters only requested properties to the put request.
                transformForServer : function(){
                    return angular.copy(this);
                },
                assignTaskState: function (task, state) {
                    var toServerObj = this.transformForServer();
                    task.state = state;
                    toServerObj.tasks = [task];
                    return toServerObj.put();
                }
            });
        });
        // It's also possible to extend the collection methods using Restangular.extendCollection().
        return Restangular.all('cases');
    }]);