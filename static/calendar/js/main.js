$(function() {

	rome(inline_cal, {time: false, inputFormat: 'DD / MM / YYYY'}).on('data', function (value) {
	  result.value = value;
	});

});