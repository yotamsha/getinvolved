angular.module('app.models.case.viewModelExpanders',['uz.mailto'])
	.service('CaseEmailShareExpander',['$translate','Mailto', function($translate, Mailto){
		function expandCases(cases){
			$translate(['case_share.email.subject','case_share.email.body']).then(function(translataions){
				var recepient = "sheker-kolsheu@getinvolved.org.il";
				var options = {
					subject: translataions["case_share.email.subject"],
					body: translataions["case_share.email.body"]
				};
				
				var href = Mailto.url(recepient, options);
			
				_.each(cases, function(_case){
					_case.mailtoLink = href;
				});
			});
		}
		
		return {
			expandCases: expandCases
		}
	}]);
	