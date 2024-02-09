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

// Define the selectors for easier reuse and better performance
var $dateStart = $("form input[name='dateStart']");
var $dateStop = $("form input[name='dateStop']");
var $submitBtn = $("input[name='appoinment_submit']");

// Define a function to update the border color and error message
function updateInput(input, color, message) {
    input.css("border-color", color);
    var $errorMessage = $("#" + input.attr("name") + "ErroMessage");
    if (message) {
        $errorMessage.html(message).removeAttr("hidden");
    } else {
        $errorMessage.attr("hidden", true);
    }
}

// Check dateStart value
$dateStart.on("change", function () {
    var dateStartVal = $(this).val();
    if (dateStartVal) {
        $.ajax({
            url: "/check-date_start/" + dateStartVal,
            type: "GET",
            success: function () {
                updateInput($dateStart, "green");
            },
            error: function (response) {
                updateInput($dateStart, "red", response.responseJSON.error);
            },
        });
    }
});

// Check dateStop and dateStart values
$dateStop.add($dateStart).on("change", function () {
    var dateStopVal = new Date($dateStop.val());
    var dateStartVal = new Date($dateStart.val());
    if (dateStopVal >= dateStartVal) {
        updateInput($dateStop, "green");
        var diffDays = Math.round(Math.abs(dateStopVal - dateStartVal) / (1000 * 60 * 60 * 24)) + 1;
        $("p[name='dateDuration']").text(diffDays + " jour(s)");
        $("input[name='durationDay']").removeAttr("hidden");
    } else {
        updateInput($dateStart, "red", "La date de début ne peut être supérieur à la date de fin");
    }
});

// Enable submit button
$dateStop.add($dateStart).on("change", function () {
    if ($dateStart.val() && $dateStop.val()) {
        $submitBtn.removeAttr("disabled");
    } else {
        $submitBtn.attr("disabled", "disabled");
    }
});



  document.querySelector('[name="appoinment_submit"]').addEventListener('click', function(event) {
    event.preventDefault();

    var doctor = document.querySelector('[name="doctor"]').value;
    var dateStart = document.querySelector('[name="dateStart"]').value;
    var dateStop = document.querySelector('[name="dateStop"]').value;

    if (doctor && dateStart && dateStop) {
        fetch('/check-slot/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value
            },
            body: new URLSearchParams({
                'doctor_id': doctor,
                'date_start': dateStart,
                'date_stop': dateStop
            })
        })
        .then(response => response.json())
        .then(data => {
            if (response.ok) {
                // Handle success
                console.log(data);
            } else {
                // Handle error
                console.error(data);
            }
        });
    } else {
        alert('Please fill in all fields');
    }
});

  //end of document ready
});
