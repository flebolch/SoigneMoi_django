// jquery ready start
$(document).ready(function() {

    // Bootstrap tooltip
    if($('[data-toggle="tooltip"]').length > 0) {  // check if element exists
        $('[data-toggle="tooltip"]').tooltip();  // initialize tooltip
    }

    // Toggle collapse on click
    $("#toggle-btn").click(function(){
        $("#toggle-example").collapse('toggle'); // toggle collapse
    });

});
// jquery end