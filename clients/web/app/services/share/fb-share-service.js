angular.module('app.services.share',[])
	.service('FbShare',['$translate', function($translate){
		function shareCase(_case){
			$translate(['case_share.title','case_share.description'])
				.then(function(translations){
						FB.ui({
							method: 'feed',
							link: 'http://' + location.host + '/#/case/' + _case.id,
							description: translations["case_share.description"],
							name: translations["case_share.title"]
							//TODO: add picture property with case image URL
						}, function(response){});   
				});	
		}
		
		return {
			shareCase: shareCase
		}
	}]);
	