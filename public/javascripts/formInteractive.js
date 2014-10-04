$(document).ready(function() {
	$("#ChoiceContainer").hide();
	var inpFilled = false;
    var carrierSelected = false;
    var regionSelected = false;
    var spotSelected = false;
    $("#null").hide();

	$("#SignUp").hover(
		function () {
			$(this).css("background-color", "rgba(255,255,255,0.80)");
		},
		function () {
			$(this).css("background-color", "rgba(255,255,255,0.60)")
		}
	);

	$("#SignUp").click(function() {
		$(this).fadeOut();
		$("#ChoiceContainer").slideDown(500);
	});

	$("#PhoneNumber").change(function() {
		if($(this).val().length == 10) {
			inpFilled = true;
		}
		else {
			inpFilled = false;
		}
		if(spotSelected && regionSelected && carrierSelected && inpFilled) {
            buttonClickable();
        }
        else {
        	buttonUnclickable();
        }        			
	});

	$("#Carrier").change(function() {
		if($(this).val() != "Select Carrier") {
			carrierSelected = true;
		}
		else {
			carrierSelected = false;
		}
		if(spotSelected && regionSelected && carrierSelected && inpFilled) {
            buttonClickable();
        }
        else {
        	buttonUnclickable();
        }
	});

	$("#BigSelect").change(function() {        			
		if($(this).val()=="null") {
			regionSelected = false;
			spotSelected = false;
		}
		else {
			spotSelected = false;
			regionSelected = true;
			var region = $(this).val().split('|')[0];
			var area = $(this).val().split('|')[1];
			var parameters = {reg: region, ar: area, id: 2};
			$.get('/spots-in-area', parameters, function(data) {
				$('#spot-slot').html(data);
			});
		}
		if(spotSelected && regionSelected && carrierSelected && inpFilled) {
            buttonClickable();
        }
        else {
        	buttonUnclickable();
        }
	});

	$("#spot-slot").change(function() {                                
		if($(this).val()=="null") {
			spotSelected = false;
		} else {
			spotSelected = true;
		}
		if(spotSelected && regionSelected && carrierSelected && inpFilled) {
            buttonClickable();
        }
        else {
        	buttonUnclickable();
        }
	});

});

function buttonClickable() {
	var newHTML = '<button id="submit" type="button" onclick="postInfo();">Submit</button>';
	$('#submit-button-container').html(newHTML);
}

function buttonUnclickable() {
	var newHTML = '<button id="submit" type="button" disabled>Submit</button>';
	$('#submit-button-container').html(newHTML);
}

function postInfo() {
	var phone = $('#PhoneNumber').val();
	var carrier = $('#Carrier').val();
	var spot = $('#BigSelect').val().concat('|').concat($('#spot-slot').val());
	var info = {phoneNumber: phone, cellCarrier: carrier, location: spot};
	$.post('/add-spot', info);
}