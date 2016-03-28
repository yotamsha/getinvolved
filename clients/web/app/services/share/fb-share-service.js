angular.module('app.services.share',[])
	.service('FbShare',['$translate', function($translate){
		function shareCase(_case){
			$translate(['case_share.fb.title','case_share.fb.description'])
				.then(function(translations){
						FB.ui({
							method: 'feed',
							link: 'http://' + location.host + '/#/case/' + _case.id,
							description: translations["case_share.fb.description"],
							name: translations["case_share.fb.title"]
							//TODO: add picture property with case image URL
						}, function(response){});   
				});	
		}
		
		return {
			shareCase: shareCase
		}
	}]);
	