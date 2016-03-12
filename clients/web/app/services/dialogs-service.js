/**
 * Created by yotam on 29/1/2016.
 */
'use strict';

angular.module('app.services.dialogs-service', [])
    .service('DialogsService', ['$mdMedia','$mdDialog', function ($mdMedia, $mdDialog) {

        var dialogsMapping = {
            login : {
                controller : 'loginCtrl',
                templateUrl : 'authentication/login.html',
                actionCb : function(answer){
                },
                cancelCb : function(){
                }
            }
        }
        return {
            openDialog: function (extendWithOptions) {
                var dialogOptions = { // defaults
                    parent: angular.element(document.body),
                    //targetEvent: ev,
                    clickOutsideToClose: true,
                    bindToController : true,
                    fullscreen: $mdMedia('xs')
                };
                // extend defaults with the specific dialog defaults and then extend it with execution specific options.
                angular.extend(dialogOptions,dialogsMapping[extendWithOptions.dialog],extendWithOptions);
                window.scrollTo(0, 0);
                return $mdDialog.show(dialogOptions)// call the defined callbacks or predefined ones , or do nothing :
                    .then(extendWithOptions.actionCb || dialogsMapping[extendWithOptions.dialog].actionCb || function() {},
                        extendWithOptions.cancelCb || dialogsMapping[extendWithOptions.dialog].cancelCb || function() {});
            }

        };
    }]);