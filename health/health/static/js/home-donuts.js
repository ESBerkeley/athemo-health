var width = 250,
    height = 190,
    radius = Math.min(width, height) / 1.7;

var ARC = d3.svg.arc()
    .innerRadius(radius - 50)
    .outerRadius(radius - 30);

var HIGHLIGHT_ARC = d3.svg.arc()
    .innerRadius(radius - 50)
    .outerRadius(radius - 23);


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
 * @param parentClass - string of parent class name e.g. '.plan-col-1'
 * @param className - string of class name to append donut to, e.g ".estimated-cost-donut"
 * @param donutType - string of donut type for color, pick between "cost", "save", "zero"
 * @param data - JSON of data to be input
 * @param highlight_default_name - STRING of class name to be highlighted on default e.g. annual_premium, maternity_cost
 */
function makeSvgDonut(parentClass, className, donutType, data, highlight_default_name) {
    var svgMap = {} // a map of element name(e.g. annual_premium, doctor_cost) to the SVG path element

    if (donutType == "zero") {
        data = [{"value": 1}];
    }

    var total = 0;
    for (i in data) {
        total += data[i]["value"]
    }

    var color = d3.scale.category20();

    var pie = d3.layout.pie()
        .sort(null)
        .value(get_value);

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
        .attr("fill", function(){ return "rgb(51, 51, 51)" }) /* color of middle text */
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
        .attr("d", ARC)
    if (donutType == "cost") {
        path.attr("fill", function(d, i) { return redColor(i); });
    }  else if (donutType == "zero") {
        path.attr("fill", function(d, i) { return "#777b7e" });
    }

    // maps element name to svg object
    path.each(function(data, stuff){
        svgMap[d3.select(this).data()[0].data.name] = this;
    })

    //mouseover logic
    path.on("mouseover", function(){
        unHighlightAll(parentClass+'.cost-detail', svgMap);
        var name = d3.select(this).data()[0].data.name;
        highlightCost(parentClass+"."+name, this);
    })
    path.on("mouseout", function(){
        unHighlightAll(parentClass+'.cost-detail', svgMap);
    })

    // logic of when hovering over text, highlight donut as well
    $(parentClass+".cost-detail").unbind().hover(function(){
        unHighlightAll(parentClass+'.cost-detail', svgMap);
        var name = $(this).attr("name");
        highlightCost(parentClass+'.'+name, svgMap[name]);
    }, function(){
        unHighlightAll(parentClass+'.cost-detail', svgMap);
    });

    if (highlight_default_name) {
        unHighlightAll(parentClass+'.cost-detail', svgMap);
        //highlight segment by default
        if (highlight_default_name == "none") highlight_default_name = "annual_premium";
        highlightCost(parentClass+'.'+highlight_default_name, svgMap[highlight_default_name]);
    }
}

//highlight specific element
function highlightCost(className, svgElement) {
    d3.select(svgElement).attr("d", HIGHLIGHT_ARC);
    $(className).css({ "background-color" : "#d6e6f4", cursor: "pointer"});
}

//unhighlight all
function unHighlightAll(className, svgMap) {
    for(key in svgMap) d3.select(svgMap[key]).attr("d", ARC);
    $(className).css({ "background" : "none"});
}

/**
 * Preps the front end elements to hide the zero elements and show the right elements.
 * It then calls a function to populate the data within the d3 wheel for this specific row
 * @param data - JSON data to be input into a row
 * @param plan_num - plan number 1 ~ 3 that will have data injected.
 * @param extra_procedure - the STRING of the extra procedure name ('low_maternity_cost', 'diabetes_cost', 'hospitalization_cost', 'high_maternity_cost')
 * @param animate_change - BOOLEAN of whether or not to animate changes
 */
function fillPlan(data, plan_num, extra_procedure, animate_change) {
    var savings = data.extras.savings;
    var monthly_premium = data.extras.total_monthly_premium;
    var medal = data.fields.medal.toLowerCase();
    var plan_name = data.fields.provider.fields.name;
    var out_of_pocket_cost_array = eval(data.extras.total_out_of_pocket_cost);
    var out_of_pocket_cost_number = data.extras.out_of_pocket_cost_number;
    var deductible = data.extras.deductible;
    var coinsurance_rate = data.extras.coinsurance_rate;
    var out_of_pocket_max = data.extras.out_of_pocket_max;
    var example_procedure_costs = eval("(" + data.extras.example_procedure_cost + ")");
    var example_procedure_savings = eval("(" + data.extras.example_procedure_savings + ")");
    var extra_procedure_saving_name = extra_procedure.split("_")[0] + "_savings";

    var cost_data = {}
    for (index in out_of_pocket_cost_array ) {
        var cost = out_of_pocket_cost_array[index]
        cost_data[cost.name] = cost.value;
    }

    var plan_col = ".plan-col-" + plan_num + " ";

    $(plan_col+".learn-more").show();
    $(plan_col+".cost-detail").show();
    $(plan_col+".cost-detail.extra").hide();
    if (animate_change) $(plan_col+".cost-detail.extra."+extra_procedure).fadeIn();
    else $(plan_col+".cost-detail.extra."+extra_procedure).show();
    $(plan_col+".example-procedure").show();

    $(plan_col+".plan-name").text(plan_name).removeClass("zero");
    $(plan_col+".medal")
        .text(medal)
        .attr("class", "medal "+medal)
    $(plan_col+".monthly-premium").html("$" + monthly_premium ).removeClass("zero");

    // assign the values for cost details
    $(plan_col+".annual_premium .value").html("$" + cost_data['annual_premium']);
    $(plan_col+".doctor_cost .value").html("$" + cost_data['doctor_cost']);
    $(plan_col+".prescription_cost .value").html("$" + cost_data['prescription_cost']);

    // plan details data
    $(plan_col+".plan-details .deductible .value").text("$" + deductible);
    $(plan_col+".plan-details .out-of-pocket-max .value").text("$" + out_of_pocket_max);
    $(plan_col+".plan-details .co-insurance-rate .value").text(coinsurance_rate*100 + "%");

    var new_out_of_pocket = out_of_pocket_cost_array.slice(0); //copy array and attempt add new cost
    if (extra_procedure == "none") {
        $(plan_col+".procedure-breakdown .total").html("Uninsured Cost: $0");
        $(plan_col+".procedure-breakdown .you-pay").html("You Pay: $0");
    } else {
        $(plan_col+"." + extra_procedure + " .value").html("$" + example_procedure_costs[extra_procedure]);
        $(plan_col+".procedure-breakdown .total").html("Uninsured Cost: $" + (example_procedure_costs[extra_procedure] +
            example_procedure_savings[extra_procedure_saving_name]));
        $(plan_col+".procedure-breakdown .you-pay").html("You Pay: $" + example_procedure_costs[extra_procedure]);

        var new_cost = {name: extra_procedure, value: example_procedure_costs[extra_procedure]};
        new_out_of_pocket.push(new_cost);
    }

    makeSvgDonut(plan_col, plan_col + ".estimated-cost-donut", "cost", new_out_of_pocket, extra_procedure);
//    $(".plan-modal-"+plan_num + " .cost").text(data.plan_name);
    $(".plan-modal-"+plan_num + ".modal-title").text("Go to " + plan_name);

}

/**
 * Fill a plan number with zero data to put no information available
 * @param plan_num
 */
function fillZeroPlan(plan_num) {
    var plan_col = ".plan-col-" + plan_num + " ";
    $(plan_col+".learn-more").hide();
    $(plan_col+".cost-detail").hide();
    $(plan_col+".example-procedure").hide();

    $(plan_col+".plan-name").text("No plan available").addClass("zero");
    $(plan_col+".medal").attr("class", "medal nonzero")
        .text("---")
        .attr("class", "medal zero")
    $(plan_col+".monthly-premium").html("$0").addClass("zero");
    $(plan_col+".plan-details .deductible .value").text("$0");
    $(plan_col+".plan-details .out-of-pocket-max .value").text("$0");
    $(plan_col+".plan-details .co-insurance-rate .value").text("0%");

    makeSvgDonut("", plan_col + ".estimated-cost-donut", "zero", {}, false);
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
    if (i == 0) return '#2a93a3'
    if (i == 1) return '#2a56a3'
    if (i == 2) return '#00bf99'
    if (i == 3) return '#800000'
}
