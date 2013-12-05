$(document).ready(function(){
	var url = document.URL;
	// Kind of hacky for now...
	if (url.indexOf('about') >= 0) {
			$('#about').addClass('active');
	} else if (url.indexOf('household_info') >= 0) {
			$('#household_info').addClass('active');
	} else {
			$('#home').addClass('active');
	}
});