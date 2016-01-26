/**
 * Created by yotam on 8/1/2016.
 */
'use strict';

angular.module('app.services.data-access.data-access-service', [])

    .service('appData', ['$http', function ($http) {
        var isDebug = true;

        var base = "http://127.0.0.1:1337/"
        var appData = {
            post: function (path, data) {
                return $http.post(base + path, data)

            },
            getAll: function (model) {
                return $http.get(base + model.toLowerCase())
            },
            save: function (model, data) {
                return $http.post(base + model.toLowerCase(), data)
            },
            saveOrUpdate : function(model, data){
                if (!data.id){
                    return this.save(model.toLowerCase(),data);
                } else {
                    return $http.put(base + model.toLowerCase() + "/" + data.id, data)
                }
            },
            remove : function(model,data){
                if (data.id){
                    return $http.delete(base + model.toLowerCase() + "/" + data.id, data)
                } else {
                    return false;
                }
            }

        };
        return appData;
    }]);
