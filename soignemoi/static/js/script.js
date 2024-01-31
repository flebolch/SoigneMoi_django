$(document).ready(function () {
  // Populating the intervention dropdown
  $("form select[name='service']").on("change", function () {
    var $this = $(this);
    if ($this.val() != "") {
      $("form select[name='intervention']")
        .prop("disabled", false)
        .removeAttr("hidden");
      $("div[name='intervention_medecin']").removeAttr("hidden");
      $.ajax({
        url: "/get-interventions/" + $this.val(),
        type: "GET",
        success: function (resp) {
          var $interventionDropdown = $("form select[name='intervention']");
          $interventionDropdown.empty();
          $interventionDropdown.append(
            new Option("Sélectionnez une intervention", "")
          );
          resp.interventions.forEach(function (intervention) {
            var optionText =
              intervention.name + " - " + intervention.duration + " jours";
            $interventionDropdown.append(
              new Option(optionText, intervention.id)
            );
          });
        },
        error: function (resp) {
          console.log(resp);
        },
      });
    } else {
      $("form select[name='intervention']").empty();
      $("form select[name='intervention']").prop("disabled", true);
    }
  });

  // Populating the doctor dropdown
  $("form select[name='service']").on("change", function () {
    var $this = $(this);
    if ($this.val() != "") {
      $("form select[name='doctor']").prop("disabled", false);
      $.ajax({
        url: "/get-doctors/" + $this.val(),
        type: "GET",
        success: function (resp) {
          var $doctorDropdown = $("form select[name='doctor']");
          $doctorDropdown.empty();
          $doctorDropdown.append(new Option("Sélectionnez un médecin", ""));
          resp.doctors.forEach(function (doctor) {
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
      $("form select[name='doctor']").prop("disabled", true);
    }
  });

  //display date and validation fields
  // When either the doctor or intervention dropdown changes
  $("form select[name='doctor'], form select[name='intervention']").on(
    "change",
    function () {
      // Get the selected doctor and intervention
      var $selectedDoctor = $("form select[name='doctor']").val();
      var $selectedIntervention = $("form select[name='intervention']").val();

      // If both the doctor and intervention are selected
      if ($selectedDoctor != "" && $selectedIntervention != "") {
        // Remove the hidden attribute from the date and validation divs
        $("div[name='dates_validation']").removeAttr("hidden");
      } else {
        $("div[name='dates_validation']").attr("hidden", true);
      }
    }
  );

  //enable submit button appoinment_submit

  $("form input[name='dateStart'], form input[name='dateStop']").on(
    "change",
    function () {
      console.log("The selected option has changed.");
      console.log("change");
      var $selectedDateStart = $("form input[name='dateStart']").val();
      var $selectedDateStop = $("form input[name='dateStop']").val();
      console.log($selectedDateStop);
      if ($selectedDateStart != "" && $selectedDateStop != "") {
        $("input[name='appoinment_submit']").removeAttr("disabled");
    } else {
      $("input[name='appoinment_submit']").attr("disabled", "disabled");
    }
    }
  );

  //end of document ready
});
