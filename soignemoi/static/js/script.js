$(document).ready(function () {

  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');


  // Populating the intervention dropdown
  $("form select[name='service']").on("change", function () {
    var $this = $(this);
    var serviceInput = $("form select[name='service']");
    if ($this.val() != "") {
      $("p[name='selectServiceErrorMessage']").attr("hidden", true);
      serviceInput.css("border-color", "");
      $("form select[name='intervention']")
        .prop("disabled", false)
      $.ajax({
        url: "/get-interventions/" + $this.val(),
        type: "GET",
        Headers: {
          "X-CSRFToken": csrftoken,
        },
        success: function (resp) {
          var $interventionDropdown = $("form select[name='intervention']");
          $interventionDropdown.empty();
          $interventionDropdown.append(
            new Option("Sélectionnez une intervention", "")
          );
          resp.interventions.forEach(function (intervention) {
            var optionText =
              intervention.name;
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
        Headers: {
          "X-CSRFToken": csrftoken,
        },
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
  
  //check if the fields are filled
  $("form select[name='doctor']").on("change", function () {
    var $this = $(this);
    var doctorInput = $("form select[name='doctor']");
    if ($this.val() != "") {
      $("p[name='selectDoctorErrorMessage']").attr("hidden", true);
      doctorInput.css("border-color", "");
    }
  });

  $("form select[name='intervention']").on("change", function () {
    var $this = $(this);
    var interventionInput = $("form select[name='intervention']");
    if ($this.val() != "") {
      $("p[name='selectInterventionErrorMessage']").attr("hidden", true);
      interventionInput.css("border-color", "");
    }
  });

  $("input[name='dateStart']").on("change", function () {
    var dateStartVal = $(this).val();
    var dateStartInput = $("input[name='dateStart']");
    $("p[name='dateStartErroMessage']").attr("hidden", true);
    dateStartInput.css("border-color", "");
    var dateStopInput = $("input[name='dateStop']");
    if (!dateStopInput.val()) {
      dateStopInput.val(dateStartVal);
      $("p[name='dateStopErroMessage']").attr("hidden", true);
      dateStopInput.css("border-color", "");
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

  var data;
  var requestDataCopy;
  //looking for missing fields in the form
    var buttonBooking = $("button[name='submitDateStopAndStart']");
    buttonBooking.click(function() {
      var service = null;
      var doctor = null;
      var intervention = null;
      var dateStart = null;
      var dateStop = null;

      var selectedSertvice = Number($("select[name='service']").val());
      if (Number.isInteger(selectedSertvice) && selectedSertvice > 0) {
        service=selectedSertvice;
      } else { 
        $("p[name='selectServiceErrorMessage']").removeAttr("hidden");
        $("select[name='service']").css("border-color", "red");
        $("#selectServiceErrorMessage").text("Veuillez sélectionner un service")
      }
      var selectedDoctor = Number($("select[name='doctor']").val());
      if (Number.isInteger(selectedDoctor) && selectedDoctor > 0) {
        doctor=selectedDoctor;
      } else {
        $("p[name='selectDoctorErrorMessage']").removeAttr("hidden");
        $("select[name='doctor']").css("border-color", "red");
        $("#selectDoctorErrorMessage").text("Veuillez sélectionner un médecin")
      }

      var selectedIntervention = Number($("select[name='intervention']").val());
      if (Number.isInteger(selectedIntervention) && selectedIntervention > 0) {
        intervention=selectedIntervention;
      } else {
        $("p[name='selectInterventionErrorMessage']").removeAttr("hidden");
        $("select[name='intervention']").css("border-color", "red");
        $("#selectInterventionErrorMessage").text("Veuillez sélectionner une intervention")
      }

      var dateStartInput = $("input[name='dateStart']");
      var dateStartVal = dateStartInput.val();
      var dateStart = new Date(dateStartVal);
      console.log(dateStart);
      if (isNaN(dateStart.getTime())) {
          $("p[name='dateStartErroMessage']").removeAttr("hidden");
          $("input[name='dateStart']").css("border-color", "red");
          $("#dateStartErroMessage").text("Veuillez sélectionner une date de début");
      } else {
          dateStart = dateStartVal;
      }

      var dateStopInput = $("input[name='dateStop']");
      var dateStopVal = dateStopInput.val();
      var dateStop = new Date(dateStopVal);
      console.log(dateStop);
      if (isNaN(dateStop.getTime())) {
          $("p[name='dateStopErroMessage']").removeAttr("hidden");
          $("input[name='dateStop']").css("border-color", "red");
          $("#dateStopErroMessage").text("Veuillez sélectionner une date de fin");
      } else {
          dateStop = dateStopVal;
      }
      
      if (service && doctor && intervention && dateStart && dateStop) {
         data = {
          service: service,
          doctor: doctor,
          intervention: intervention,
          dateStart: dateStart,
          dateStop: dateStop,
        };
        console.log(data);
        $.ajax({
          url: "/create-appointment/" + service + "/" + intervention + "/" + doctor + "/" + dateStart + "/" + dateStop + "/",
          type: "GET",
          headers: {
              "X-CSRFToken": csrftoken
          },
          success: function(response) {
              $("div[name='appoinmentValidation']").removeAttr("hidden");
              $("p[name='validation']").text(response.message).show();
              $("div[name='appoinmentValidation']").attr('tabindex', 0).focus();
              // Copy the request data
              requestDataCopy = Object.assign({}, data);
          },
          error: function (jqXHR) {
            if (jqXHR.status == 400) {
              $("div[name='appoinmentValidation']").attr("hidden", true);
              var response = JSON.parse(jqXHR.responseText);
              if (response.errorDateStart) {
                $("#dateStartErroMessage").text(response.errorDateStart).show();
                $("p[name='dateStartErroMessage']").removeAttr("hidden");
                $("input[name='dateStart']").css("border-color", "red");
              } else if (response.errorDateStop) {
                $("#dateStopErroMessage").text(response.errorDateStop).show();
                $("p[name='dateStopErroMessage']").removeAttr("hidden");
                dateStopInput.css("border-color", "red");
              }
            }
          },
        });
      }
  });

  var buttonSubmitAppointment = $("button[name='submitAppointment']");
  buttonSubmitAppointment.click(function() {
    $.ajax({
      url: "/register-appointment/" + requestDataCopy.intervention + "/" + requestDataCopy.doctor + "/" + requestDataCopy.dateStart + "/" + requestDataCopy.dateStop + "/",
      // url: "/register_appointment/",
      type: "GET",
      headers: {
        "X-CSRFToken": csrftoken,
        "Content-Type": "application/json"
      },
      // data: JSON.stringify(requestDataCopy),
      success: function(response) {
        console.log(response);
      },
      error: function(jqXHR) {
        if (jqXHR.status == 400) {
          var response = JSON.parse(jqXHR.responseText);
          console.log(response);
        } else if (jqXHR.status == 405) {
          var response = JSON.parse(jqXHR.responseText);
          console.log(response);
        }
      }
    });
  });
});
