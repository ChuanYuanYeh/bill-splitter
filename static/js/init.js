//Hook up the tweet display

$(document).ready(function() {
						   
	$(".countdown").countdown({
				date: "01 jan 2021 00:00:00",
				format: "on"
			},
			
			function() {
				// callback function
			});

});	