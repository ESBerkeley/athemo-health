$(document).ready(function(){
    //fancy select initialize
    $('.procedure').fancySelect();

    $("#zipcode").on("change keyup paste", function() {
        if ( $(this).val().length >= 5 ) showMoreInfoForm();
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
    if (checkIpad()) {
        createMobileButton();
    }
    procedureChange();
})

var PLAN_DATA = {"1": {}, "2": {}, "3": {} } //hash that maps plan number (e.g. 1,2,3 to the JSON of plan data)

/**
 * main function to handle logic of adding person rows
 */
function adjustPersonRows() {

	var peopleCount = 1;
    
    $("#add_person").click(function() {
    	$(".delete_person").css("display", "none");
    	peopleCount++;
    	$("#person_rows").append(
			"<div id='person_" + peopleCount + "' class='person-row'> \
                <div class='person-label'>Person " + peopleCount + "'s Age</div> \
                <div class='row'> \
										<div class='col-xs-11 col-md-11'> \
												<input id='input_person_" + peopleCount + "' type='text' class='form-control' name='age'/> \
										</div> \
										<div class='delete_person col-xs-1 col-md-1' personId=" + peopleCount + " > \
                    		<span class='glyphicon glyphicon-remove'></span> \
                		</div> \
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
    $(".info-col input").on("input", function(){
        window.clearTimeout(requestTimer);
        requestTimer = window.setTimeout(sendRequest, 1000);
    });
}


/**
 * main fn to sendRequest() on focus out
 */
function captureFocusOut() {
    $(".info-col").on("focusout", "input", function(event){
        if (event.target.id === "annual-income") {
            var value = formatDollar(event.target.value);
            if (!value) {
                event.target.value = "";
            } else {
                event.target.value = value;
            }
        }
        window.clearTimeout(requestTimer);
        sendRequest();
    });
}

/**
 * helper fn for sending the ajax request
 */
function sendRequest() {

    if ($("#zipcode").val() === "" || $("#zipcode").val().length != 5) {   // don't send request if ZIP code field is empty or not 5 digit
       return;
    }

    // get form data
    var formData = $("form#info-form").serialize();
    // TODO come up with a more elegant solution to parse number
    formData = formData.split(encodeURIComponent(",")).join("");    // removes commas from annual household income input field
    $.ajax({
        url: "/ajax/get_plans",
        data: formData
    }).done(function(data){

        if ($.isEmptyObject(data)) {
            $(".no-zip-code").addClass("show");
            $(".plan-parent").addClass("no-data");
        } else {
            $(".no-zip-code").removeClass("show");
            $(".plan-parent").removeClass("no-data");
            for (var i = 0; i < 3; i++) {
                if (i < data.length) {
                    var procedure_type = $(".plan-col-" + (i+1) + " select.procedure").val();
                    fillPlan(data[i], i+1, procedure_type, false);
                    fillModal(data[i], i+1);
                    PLAN_DATA[i+1] = data[i];
                } else {
                    fillZeroPlan(i+1);
                    PLAN_DATA[i+1] = {};
                }
            }
        }
    })
    .fail(function(){

    })
}

function fillModal(data, plan_num) {
    var monthly_premium = data.extras.total_monthly_premium;
    var plan_name = data.fields.provider.fields.name;
    var plan_url = data.fields.provider.fields.url;
    var deductible = data.extras.deductible;
    var coinsurance_rate = data.extras.coinsurance_rate;
    var out_of_pocket_max = data.extras.out_of_pocket_max;
    var medal = data.fields.medal;
    var medal_style = data.fields.medal.toLowerCase();
    $("#plan-modal-" + plan_num + " .cost").html(monthly_premium);
    $("#plan-modal-" + plan_num + " .modal-title").html(plan_name);
    $("#plan-modal-" + plan_num + " .btn").html("Go To " + plan_name);
    $("#plan-modal-" + plan_num + " .btn").attr("href", plan_url);
    $("#modal-medal-" + plan_num).removeClass();
    $("#modal-medal-" + plan_num).addClass("medal");
    $("#modal-medal-" + plan_num).addClass(medal_style);
    $("#modal-medal-" + plan_num).html(medal + " Plan Details");
    $("#modal-deductible-" + plan_num).html("$ " + deductible);
    $("#modal-out-of-pocket-max-" + plan_num).html("$ " + out_of_pocket_max);
    $("#modal-co-insurance-" + plan_num).html(coinsurance_rate * 100 + "%");
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

// creates "see more" button to view more insurance plans
function createMobileButton() {

    $(".wrapper").append(
        "<div id='seeMoreButtonWrapper' class='btn-lg'><div id='seeMoreButton' class='glyphicon glyphicon-chevron-right'></div></div> \
        <div id='seeLessButtonWrapper' class='btn-lg'><div id='seeLessButton' class='button-hidden glyphicon glyphicon-chevron-left'></div></div>"
    );

    $(".wrapper").on("click", "#seeMoreButtonWrapper", function() {
        setTimeout(function () {
            $(".plan-parent").addClass("plan-parent-show");
        }, 500);
        $(".info-col").addClass("info-col-hidden");
        $("#seeMoreButton").addClass("button-hidden");
        $("#seeLessButton").removeClass("button-hidden");
    })

    $(".wrapper").on("click", "#seeLessButtonWrapper", function() {
        setTimeout(function () {
            $(".info-col").removeClass("info-col-hidden")
            $(".plan-col").removeClass("plan-col-show");
        }, 500);
        $("#seeMoreButton").removeClass("button-hidden");
        $("#seeLessButton").addClass("button-hidden");
    })
}

// helper function to check if user is using iPad
function checkIpad() {
    return navigator.userAgent.match(/iPad/i) != null;
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
    if (isNaN(number)) {
        return false;
    } else {
        return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

/**
 * applies jquery logic that on select change, change the content of column
 */
function procedureChange() {
    $("select.procedure").change(function(){
        var procedure_type = $(this).val();
        var col_num = $(this).parents(".plan-col").attr("plan-col");
        fillPlan(PLAN_DATA[col_num], col_num, procedure_type, true);
    })
}