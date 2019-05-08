$(document).ready(function() {

	$('form').on('submit', function(event) {
		$.ajax({
			data : {
				zipCode : $('#zipInput').val()
			},
			type : 'POST',
			url : '/google'
		})
//		.done(function(data) {
//      if (data.error) {
//        // $('#cardValue').hide();
//        $('#cardValue-house').hide();
//        $('#cardValue-income').hide();
//        $('#cardValue-pop').hide();
//        $('#cardValue-edu').hide();
//				alert("Try another ZIP Code!");
//        console.log(data.error);
//			}
//			else {
//        // console.log(data.zipCode);
//        // $('#cardValue').show();
//        $('#cardValue-house').text(data.houseValue).show();
//        $('#cardValue-income').text(data.incomeValue).show();
//        $('#cardValue-pop').text(data.populationValue).show();
//        $('#cardValue-edu').text(data.educationValue).show();
//        console.log(data);
//
//        // $('#successAlert').text(data.name).show();
//				// $('#errorAlert').hide();
//			}
//		});

		event.preventDefault();

	});
});
