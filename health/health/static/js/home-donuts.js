/**
 * main fn to run d3 to generate donut charts
 */
function generateZeroPlan() {
    var dataset = {
      apples: [{value: 53245, name: "cost-annual-premium"},{value: 50000, name: "cost-something-premium"}]
    };

    fillZeroPlan(1);
    fillZeroPlan(2);
    fillZeroPlan(3);

}

/**
 * Helper fn that makes a d3 donut
 * @param className - string of class name to append donut to, e.g ".estimated-cost-donut"
 * @param donutType - string of donut type for color, pick between "cost", "save", "zero"
 * @param data - JSON of data to be input
 * @param total - sum of all the values in data
 */
function makeSvgDonut(parentClass, className, donutType, data, total) {
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
        .innerRadius(radius - 50)
        .outerRadius(radius - 23);

    $(className).html("");

    var svg = d3.select(className).append("svg")
    .attr("width", width)
    .attr("height", height)
    .append("g")
    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    var gnodes = svg.selectAll("g.gnode")
        .data(pie(data))
        .enter().append("g")
        .attr("class", "arc");

    //middle text
    if (donutType == "cost") {
        gnodes.append("text")
        .style("text-anchor", "middle")
        .attr("dy", "10px")
        .attr("class","estimated-number")
        .text(function(d){ return "$" + total })
        .attr("fill", function(){ return "#b00" }) /* color of middle text */
    }  else if (donutType == "zero") {
        gnodes.append("text")
        .style("text-anchor", "middle")
        .attr("dy", "10px")
        .attr("class","estimated-number")
        .text(function(d){ return "$0" })
        .attr("fill", function(){ return "#777b7e" })
    }

    //donut styling
    var path = gnodes.append("path")
        .style("cursor", "pointer")
        .attr("d", arc)
    if (donutType == "cost") {
        path.attr("fill", function(d, i) { return redColor(i); });
    }  else if (donutType == "zero") {
        path.attr("fill", function(d, i) { return "#777b7e" });
    }


    //mouseover logic
    path.on("mouseover", function(){
        d3.select(this).attr("d", highlightArc);
        var name = d3.select(this).data()[0].data.name;
        $(parentClass + "." + name).css({ "background-color" : "#d6e6f4"});
        //$("#"+name).css("font-weight", "bold")
    })
    path.on("mouseout", function(){
        d3.select(this).attr("d", arc);
        var name = d3.select(this).data()[0].data.name;
        $(parentClass + "." + name).css({ "background" : "none"});
    })
}

/**
 * Preps the front end elements to hide the zero elements and show the right elements.
 * It then calls a function to populate the data within the d3 wheel for this specific row
 * @param data - JSON data to be input into a row
 * @param plan_num - plan number 1 ~ 3 that will have data injected.
 */
function fillPlan(data, plan_num) {
    var savings = data.extras.savings;
    var monthly_premium = data.fields.price;
    var medal = data.fields.medal.toLowerCase();
    var plan_name = data.fields.provider.fields.name;
    var out_of_pocket_cost_array = eval(data.extras.total_out_of_pocket_cost);
    var out_of_pocket_cost_number = data.extras.out_of_pocket_cost_number;
    var cost_data = {}
    for (index in out_of_pocket_cost_array ) {
        var cost = out_of_pocket_cost_array[index]
        cost_data[cost.name] = cost.value;
    }

    var plan_col = ".plan-col-" + plan_num + " ";

    $(plan_col+".zero").hide();
    $(plan_col+".nonzero").show();
    $(plan_col+".learn-more").show();
    $(plan_col+".cost-detail").show();

    $(plan_col+".plan-name.nonzero").text(plan_name);
    $(plan_col+".medal.nonzero").attr("class", "medal nonzero")
        .text(medal)
        .addClass(medal)
    $(plan_col+".monthly-premium.nonzero").html("$" + monthly_premium );

    // assign the values for cost details
    $(plan_col+".annual_premium .value").html("$" + cost_data['annual_premium']);
    $(plan_col+".doctor_cost .value").html("$" + cost_data['doctor_cost']);
    $(plan_col+".prescription_cost .value").html("$" + cost_data['prescription_cost']);


    var dataset2 = {
      apples: [{value: 2000, name: "cost-annual-premium"},{value: 1700, name: "cost-something-premium"}]
    };

    makeSvgDonut(plan_col, plan_col + ".estimated-cost-donut", "cost", out_of_pocket_cost_array, out_of_pocket_cost_number);
//    makeSvgDonut(plan_col + ".estimated-save-donut", "save", dataset2.apples);
//    $(".plan-modal-"+plan_num + " .cost").text(data.plan_name);
    $(".plan-modal-"+plan_num + ".modal-title").text("Go to " + plan_name);

}

/**
 * Fill a plan number with zero data to put no information available
 * @param plan_num
 */
function fillZeroPlan(plan_num) {
    var plan_col = ".plan-col-" + plan_num + " ";
    $(plan_col+".nonzero").hide();
    $(plan_col+".zero").show();
    $(plan_col+".learn-more").hide();
    $(plan_col+".cost-detail").hide();

    makeSvgDonut("", plan_col + ".estimated-cost-donut", "zero", {});
    makeSvgDonut("", plan_col + ".estimated-save-donut", "zero", {});
}

/**
 * Helper function for generate_donuts
 * @param d
 */
function get_value(d) {
    return d.value;
}

/**
 * helper function given an index 0~2 returns a shade of red
 * @param i
 */
function redColor(i) {
    if (i == 0) return '#ff0000'
    if (i == 1) return '#aa0000'
    if (i == 2) return '#880000'
}

/**
 * helper function given an index 0~2 returns a shade of green
 * @param i
 */
function greenColor(i) {
    if (i == 0) return '#6ddec4'
    if (i == 1) return '#2aba99'
    if (i == 2) return '#219077'
}