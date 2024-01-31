$(document).ready(function() {
    $("form select[name='service']").on("change", function () {
        var $this = $(this);
        if ($this.val() != "") {
            $.ajax({
                url: "/get-interventions/" + $this.val(),
                type: "GET",
                success: function (resp) {
                    var $interventionDropdown = $("form select[name='intervention']");
                    $interventionDropdown.empty();
                    resp.interventions.forEach(function(intervention) {
                        var optionText = intervention.name + " - " + intervention.duration + " jours";
                        $interventionDropdown.append(new Option(optionText, intervention.id));
                    });
                },
                error: function (resp) {
                    console.log(resp);
                },
            });
        } else {
            $("form select[name='intervention']").empty();
        }
    });
});