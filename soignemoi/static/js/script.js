$(document).ready(function() {
    // Populating the intervention dropdown
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

    // Populating the doctor dropdown
    $("form select[name='service']").on("change", function () {
        var $this = $(this);
        if ($this.val() != "") {
            $.ajax({
                url: "/get-doctors/" + $this.val(),
                type: "GET",
                success: function (resp) {
                    var $doctorDropdown = $("form select[name='doctor']");
                    $doctorDropdown.empty();
                    resp.doctors.forEach(function(doctor) {
                        var optionText = doctor.doctorFullName + " - " + doctor.speciality;
                        $doctorDropdown.append(new Option(optionText, doctor.id));
                    });
                },
                error: function (resp) {
                    console.log(resp);
                },
            });
        } else {
            $("form select[name='doctor']").empty();
        }
    });

//end of document ready    
});