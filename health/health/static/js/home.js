$(document).ready(function(){
		$("#zipcode").on("change keyup paste", function() {
				showMoreInfoForm();
		});
		
		$(".more-arrow").on("click", function() {
				showMoreInfoForm();
		});
    // all inputs in info col must be numbers
    $(".info-col").on("keypress", "input", function(event){
        return isNumberKey(event);
    });

//    var highestCol = Math.max($('.info-col').height(),$('.data-col').height());
//    $('.standard-col').height(highestCol);

    // fill the 3 cols with empty data
    fillZeroPlan(1);
    fillZeroPlan(2);
    fillZeroPlan(3);

    // js logic for the info col
    adjustPersonRows();
    captureKeyPress();
    captureFocusOut();
    buttonMedalLogic();

})


/**
 * main function to handle logic of adding person rows
 */
function adjustPersonRows() {

	var peopleCount = 1;
    
    $("#add_person").click(function() {
    	$(".delete_person").css("display", "none");
    	peopleCount++;
    	$("#person_rows").append(
			"<div id='person_" + peopleCount + "' class='row person-row'> \
                <div class='col-md-4 person-label'>Person " + peopleCount + "</div> \
                <div class='col-md-2 age-label'>Age</div> \
                <div class='col-md-5'> \
                    <div> \
                        <input id='input_person_" + peopleCount + "' type='text' class='form-control input-sm' name='age'/> \
                    </div> \
                </div> \
                <div class='delete_person' personId=" + peopleCount + " > \
                    <div class='glyphicon glyphicon-remove'></div> \
                </div> \
            </div>"
		);
        $("#input_person_" + peopleCount).focus();
    })

    $("#person_rows").on("click", ".delete_person", function() {
    	peopleCount--;
    	var personId = $(this).attr("personId");
    	$("#person_" + personId).remove();
    	$("#person_" + peopleCount + " .delete_person").css("display", "inherit");
        window.clearTimeout(requestTimer);
        sendRequest();
    })
}

var requestTimer;

/**
 * main fn to sendRequest() after 1s of key input
 */
function captureKeyPress() {
    $(".info-col").on("change keyup paste", "input", function(event){
        if ( event.which == 13 ) {
            event.preventDefault();
        }
        if ( !( event.which > 31 && (event.which < 48 || event.which > 57)) ) {
            window.clearTimeout(requestTimer);
            requestTimer = window.setTimeout(sendRequest, 1000);
        }
    });
}


/**
 * main fn to sendRequest() on focus out
 */
function captureFocusOut() {
    $(".info-col").on("focusout", "input", function(event){
        if (event.target.id === "annual-income") {
            event.target.value = formatDollar(event.target.value);
        }
        window.clearTimeout(requestTimer);
        sendRequest();
    });
}

/**
 * helper fn for sending the ajax request
 */
function sendRequest() {
    // get form data
    var formData = $("form#info-form").serialize();
    // TODO come up with a more elegant solution to parse number
    formData = formData.split(encodeURIComponent(",")).join("");    // removes commas from annual household income input field
    $.ajax({
        url: "/ajax/get_plans",
        data: formData
    }).done(function(data){
        for (var i = 0; i < 3; i++) {
            if (i < data.length) fillPlan(data[i], i+1);
            else fillZeroPlan(i+1);
        }
    })
    .fail(function(){

    })
}



/**
 * main fn to run logic of medal buttons being clicked
 */
function buttonMedalLogic() {
    $(".medal-select").click(function(){
        $(".medal-select").removeClass("active");
        $(this).addClass("active");
        var medal = $(this).attr("id");
        $("#select-medal").val(medal);
        sendRequest();
    })
}

/**
 * helper fn that gets called within the main block
 * @param evt
 * @returns {boolean}
 */
function isNumberKey(evt) {
     var charCode = (evt.which) ? evt.which : event.keyCode
     if (charCode == 44 && evt.target.id === "annual-income") // allow comma only for annual income input (for dollar formatting)
        return true;
     if (charCode > 31 && (charCode < 48 || charCode > 57))
        return false;

     return true;
}

function showMoreInfoForm() {
		$(".more-info").fadeIn(300);
		$(".more-arrow").hide();
}

/*
    function that parses dollar formatting for annual household income input field
    returns parsed number or NaN
    *not used for now
*/
function parseDollar(number) {
    number = parseInt(number.split(",").join(""));
    return number;
}
/*
    function that formats number for household income field
    e.g. 12345 -> 12,345
*/
function formatDollar(number) {
    number = parseDollar(number);
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}