/**
 * Created by yotam on 20/2/2016.
 */
/**
 * Model structure inspired by:
 * http://blog.shinetech.com/2014/02/04/rich-object-models-and-angular-js/
 */
angular.module('app.models.case')
    /**
     * This is a model wrapper that includes the business logic for a Case.
     */
    .factory('CaseModel', [function () {
        return {
            chooseDefaultImage: function () {
                var DEFAULT_TASKS_IMAGES_NUM = 9;
                return "assets/img/tasks_defaults/task" + (Math.floor(Math.random() * DEFAULT_TASKS_IMAGES_NUM) + 1) + ".jpg";
            }
        };
    }])
