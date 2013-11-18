$(document).ready(function(){
    $(".chosen-select").chosen({
        no_results_text: "Sorry, we don't support that state yet."
    });

    $(".info-col").on("keypress", "input", function(event){
        return isNumberKey(event);
    });

//    var highestCol = Math.max($('.info-col').height(),$('.data-col').height());
//    $('.standard-col').height(highestCol);

    generateDonuts();
    adjustPersonRows();
    captureKeyPress();
    captureFocusOut();
    buttonMedalLogic();
})

/**
 * Helper function for generate_donuts
 * @param d
 */
function get_value(d) {
    return d.value;
}

/**
 * main fn to run d3 to generate donut charts
 */
function generateDonuts() {
    var dataset = {
      apples: [{value: 53245, name: "cost-annual-premium"},{value: 50000, name: "cost-something-premium"}]
    };

    makeSvgDonut(".plan-col-1 .estimated-cost-donut", "zero", {});
    makeSvgDonut(".plan-col-1 .estimated-save-donut", "zero", {});

    makeSvgDonut(".plan-col-2 .estimated-cost-donut", "zero", {});
    makeSvgDonut(".plan-col-2 .estimated-save-donut", "zero", {});

    makeSvgDonut(".plan-col-3 .estimated-cost-donut", "zero", {});
    makeSvgDonut(".plan-col-3 .estimated-save-donut", "zero", {});

}

/**
 * Helper fn that makes a d3 donut
 * @param className - string of class name to append donut to, e.g ".estimated-cost-donut"
 * @param donutType - string of donut type for color, pick between "cost", "save", "zero"
 * @param data - JSON of data to be input
 */
function makeSvgDonut(className, donutType, data) {
    if (donutType == "zero") {
        data = [{"value": 1}];
    }
    var width = 250,
    height = 190,
    radius = Math.min(width, height) / 1.7;

    var color = d3.scale.category20();

    var pie = d3.layout.pie()
        .sort(null)
        .value(get_value);

    var arc = d3.svg.arc()
        .innerRadius(radius - 50)
        .outerRadius(radius - 30);

    var highlightArc = d3.svg.arc()
        .innerRadius(radius - 55)
        .outerRadius(radius - 25);

    $(className).html("");

    var svg = d3.select(className).append("svg")
    .attr("width", width)
    .attr("height", height)
    .append("g")
    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    if (donutType == "zero") {
        var gnodes = svg.selectAll("g.gnode")
            .data(pie(data))
            .enter().append("g")
            .attr("class", "arc");

        //middle text
        gnodes.append("text")
            .style("text-anchor", "middle")
            .attr("dy", "10px")
            .attr("class","estimated-cost")
            .text(function(d){ return "$0" })
            .attr("fill", function(){ return "#777b7e" })

        //donut styling
        var path = gnodes.append("path")
            .attr("fill", function(d, i) { return "#777b7e" })
            .style("cursor", "pointer")
            .attr("d", arc)

        //mouseover logic
        path.on("mouseover", function(){
            d3.select(this).attr("d", highlightArc)
        })
        path.on("mouseout", function(){
            d3.select(this).attr("d", arc)
        })

    } else {

        var gnodes = svg.selectAll("g.gnode")
            .data(pie(data))
            .enter().append("g")
            .attr("class", "arc");

        //middle text
        gnodes.append("text")
            .style("text-anchor", "middle")
            .attr("dy", "10px")
            .attr("class","estimated-cost")
            .text(function(d){ return "-$2500" });

        if (donutType == "cost") {
            gnodes.attr("fill", function(){ return "#b00" }) /* color of middle text */
        } else if (donutType == "save") {
            gnodes.attr("fill", function(){ return "#2fcfaa" })
        } else if (donutType == "zero") {
            gnodes.attr("fill", function(){ return "#777b7e" })
        }

        //donut styling
        var path = gnodes.append("path")
            .attr("fill", function(d, i) { return color(i); })
            .style("cursor", "pointer")
            .attr("d", arc)

        //mouseover logic
        path.on("mouseover", function(){
            d3.select(this).attr("d", highlightArc)
            //var name = d3.select(this).data()[0].data.name
            //$("#"+name).css("font-weight", "bold")
        })
        path.on("mouseout", function(){
            d3.select(this).attr("d", arc)
        })
    }
}


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
    })
}

var requestTimer;

/**
 * main fn to sendRequest() after 1s of key input
 */
function captureKeyPress() {
    $(".info-col").on("keypress", "input", function(event){
        if ( event.which == 13 ) {
            event.preventDefault();
        }
        window.clearTimeout(requestTimer);
        requestTimer = window.setTimeout(sendRequest, 1000);
    });
}


/**
 * main fn to sendRequest() on focus out
 */
function captureFocusOut() {
    $(".info-col").on("focusout", "input", function(event){
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
    console.log(formData)
    var data = {
        plan_name: "Anthem Blue Cross",
        medal: "silver",
        money_saved: "$1000"
    }

    fillPlan(data, 1);
    fillPlan(data, 2);
    fillPlan(data, 3);
}

function fillPlan(data, plan_num) {
    var plan_col = ".plan-col-" + plan_num + " ";
    $(plan_col+".zero").hide();
    $(plan_col+".nonzero").show();
    $(plan_col+".learn-more").show();
    console.log(data.plan_name);

    $(plan_col+".plan-name.nonzero").text(data.plan_name);
    $(plan_col+".medal.nonzero").attr("class", "medal nonzero")
        .text(data.medal)
        .addClass(data.medal)

    $(plan_col+".money-saved.nonzero").text(data.money_saved);

    var dataset = {
      apples: [{value: 53245, name: "cost-annual-premium"},{value: 50000, name: "cost-something-premium"}]
    };

    makeSvgDonut(plan_col + ".estimated-cost-donut", "cost", dataset.apples);
    makeSvgDonut(plan_col + ".estimated-save-donut", "save", dataset.apples);
    $(".plan-modal-"+plan_num + " .modal-title").text(data.plan_name);
//    $(".plan-modal-"+plan_num + " .cost").text(data.plan_name);

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
     if (charCode > 31 && (charCode < 48 || charCode > 57))
        return false;

     return true;
  }