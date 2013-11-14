$(document).ready(function(){
    $(".chosen-select").chosen({
        no_results_text: "Sorry, we don't support that state yet."
    });

    var highestCol = Math.max($('.info-col').height(),$('.data-col').height());
    $('.standard-col').height(highestCol);
})
