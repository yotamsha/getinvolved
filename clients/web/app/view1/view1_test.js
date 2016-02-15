'use strict';

describe('app.view1 module', function() {
  //var $state;
  beforeEach(module('ui.router'));
  beforeEach(module('restangular'));
  beforeEach(module('pascalprecht.translate'));
  beforeEach(module('app.view1'));
  describe('view1 controller', function(){

    it('should ....', inject(function($controller,$state,$rootScope) {
      var scope = $rootScope.$new()

      //spec body
      var view1Ctrl = $controller('View1Ctrl', {
        $scope: scope,
        $state: $state //Or inject the state using the injector service and then you can use some jasmine spies to mock the function calls or just to spy on 'em.
      });
      expect(view1Ctrl).toBeDefined();
    }));

  });
});