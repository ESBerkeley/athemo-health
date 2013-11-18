$(document).ready(function(){
    $(".chosen-select").chosen({
        no_results_text: "Sorry, we don't support that state yet."
    });

    var highestCol = Math.max($('.info-col').height(),$('.data-col').height());
    $('.standard-col').height(highestCol);

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
                        <input type='text' class='form-control input-sm'/> \
                    </div> \
                </div> \
                <div class='delete_person' personId=" + peopleCount + " > \
                    <div class='glyphicon glyphicon-remove'></div> \
                </div> \
            </div>"
		);
    })

    $("#person_rows").on("click", ".delete_person", function() {
    	peopleCount--;
    	var personId = $(this).attr("personId");
    	$("#person_" + personId).remove();
    	$("#person_" + peopleCount + " .delete_person").css("display", "inherit");
    })

    generate_donuts();

})


function generate_donuts() {
    var dataset = {
      apples: [53245, 28479, 19697, 24037, 40245]
    };

    var width = 250,
        height = 220,
        radius = Math.min(width, height) / 1.7;

    var color = d3.scale.category20();

    var pie = d3.layout.pie()
        .sort(null);

    var arc = d3.svg.arc()
        .innerRadius(radius - 50)
        .outerRadius(radius - 30);

    var svg = d3.select(".estimated-cost-donut").append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    var gnodes = svg.selectAll("g.gnode")
        .data(pie(dataset.apples))
        .enter().append("g")
        .attr("class", "arc");

    //middle text
    gnodes.append("text")
        .style("text-anchor", "middle")
        .attr("dy", "10px")
        .attr("class","estimated-cost")
        .attr("fill", function(){ return "#b00"}) /* color of middle text */
        .text(function(d){ return "-$2500" });

    //donut styling
    gnodes.append("path")
        .attr("fill", function(d, i) { return color(i); })
        .attr("d", arc);

}
