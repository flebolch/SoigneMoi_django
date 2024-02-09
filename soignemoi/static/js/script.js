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

//check date function
$("input[name='dateStart']").on("change", function () {
  var dateStartVal = $(this).val();
  var dateStartInput = $("input[name='dateStart']");
  $("p[name='dateStartErroMessage']").attr("hidden", true);
  dateStartInput.css("border-color", "");
  var dateStopInput = $("input[name='dateStop']");
  if (!dateStopInput.val()) {
      dateStopInput.val(dateStartVal);
  }
});

$("input[name='dateStop']").on("change", function () {
  var dateStopVal = $(this).val();
  var dateStopInput = $("input[name='dateStop']");
  $("p[name='dateStopErroMessage']").attr("hidden", true);
  dateStopInput.css("border-color", "");

  var dateStartInput = $("input[name='dateStart']");
  if (!dateStartInput.val()) {
      dateStartInput.val(dateStopVal);
  }
});



var button = $("button[name='submitDateStopAndStart']"); // select by name attribute

if (button.length === 0) {
  console.log("Button not found");
} else {
  button.on("click", function (event) {
    event.preventDefault();
    var dateStartInput = $("input[name='dateStart']");
    var dateStopInput = $("input[name='dateStop']");
    var dateStartVal = dateStartInput.val();
    var dateStopVal = $("input[name='dateStop']").val();

    var dateStart = new Date(dateStartVal);
    var dateStop = new Date(dateStopVal);

    if (isNaN(dateStart.getTime())) {
      $("#dateStartErroMessage").text("date de début incorrecte").show();
      $("p[name='dateStartErroMessage']").removeAttr("hidden");
      dateStartInput.css("border-color", "red");
    } else if (isNaN(dateStop.getTime())) {
      $("#dateStopErroMessage").text("date de fin incorrecte").show();
      $("p[name='dateStopErroMessage']").removeAttr("hidden");
      dateStopInput.css("border-color", "red");
    } else {
      console.log("dateStart and dateStop are valid dates");
      $.ajax({
        url: '/check-dates/' + dateStartVal + '/' + dateStopVal,
        type: 'GET',
        data: {
          dateStart: dateStartVal,
          dateStop: dateStopVal
        },
        success: function(response) {
          console.log(response);
        },
        error: function(jqXHR, textStatus, errorThrown) {
          if (jqXHR.status == 400) {
              var response = JSON.parse(jqXHR.responseText);
              if (response.errorDateStart) {
                  $("#dateStartErroMessage").text(response.errorDateStart).show();
                  $("p[name='dateStartErroMessage']").removeAttr("hidden");
                  dateStartInput.css("border-color", "red");
              } else if (response.errorDateStop) {
                $("#dateStopErroMessage").text(response.errorDateStop).show();
                $("p[name='dateStopErroMessage']").removeAttr("hidden");
                dateStopInput.css("border-color", "red");
              }
          }
        }
      });
    }
  });
}

//end of document ready
});