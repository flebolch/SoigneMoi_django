$(document).ready(function () {
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      var cookies = document.cookie.split(";");
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  var csrftoken = getCookie("csrftoken");

  // Add a click event listener to the document
  document.addEventListener("click", function (event) {
    // Check if the clicked element has the class daySelected
    if (event.target.classList.contains("daySelected")) {
      // Get the text within the span
      var content = this.textContent;

      // Replace the span with its text content
      this.innerHTML = content;
    }
  });

  var buttonSelected = $("button[name='addSelected']");

  buttonSelected.click(function () {
    //put all date in an array
    var dates = [];
    var tds = document.getElementsByTagName("td");
    for (var i = 0; i < tds.length; i++) {
      if (tds[i].getElementsByClassName("daySelected").length === 1) {
        dates.push(tds[i].textContent);
      }
    }
    //if the array is not empty send the dates to the server
    if (dates.length > 0) {
      $.ajax({
        type: "POST",
        url: "/add-appointment/",
        headers: { "X-CSRFToken": csrftoken },
        data: {
          dates: dates,
          doctor_id: doctor_id,
          dateStr: dateStr,
        },
        success: function (response) {
          console.log(response);
          if (response.status === "success") {
            alert("Rendez-vous ajouté avec succès");
            location.reload();
          } else {
            alert("Une erreur s'est produite lors de l'ajout du rendez-vous");
          }
        },
        error: function (jqXHR, textStatus, errorThrown) {
          console.error("Error: " + textStatus, errorThrown);
        },
      });
    } else {
      alert("Veuillez sélectionner au moins une date");
    }
  });

  // Get doctor's planning
  var doctor_id = $("#doctor_id").val();
  var dateStr = null;

  $("form select[name='doctor']").change(function () {
    doctor_id = $(this).val();
    if (doctor_id !== "") {
      $.ajax({
        type: "GET",
        url: "/get-doctorsProfile/" + doctor_id + "/",
        headers: { "X-CSRFToken": csrftoken },
        success: function (response) {
          var doctorProfile = response.doctorProfile[0]; // Access the first element of the array
          var doctorSlots = response.timeslots;
          $('p[name="docteur_service"]').text(doctorProfile.service__name);
          $('p[name="doctor_speciality"]').text(doctorProfile.speciality);
          $('p[name="doctor_matricule"]').text(doctorProfile.matricule);
          $('p[name="doctor_email"]').text(doctorProfile.user__username);
          if (dateStr !== "") {
            fetchCalendar(getMonth(), doctor_id);
          }
        },
      });
    }
  });

  // Get the current date
  function getMonth() {
    var date = new Date();
    var year = date.getFullYear();
    var month = date.getMonth() + 1; // getMonth() returns the month number from 0 to 11
    if (month < 10) {
      month = "0" + month;
    }
    var dateStr = year + "-" + month;
    return dateStr;
  }

  function fetchCalendar(dateStr, doctor_id) {
    $.ajax({
      url: "/selectedMonth/" + dateStr + "/" + doctor_id + "/",
      type: "GET",
      headers: { "X-CSRFToken": csrftoken },
      success: function (data) {
        // The server responded with the calendar in HTML format.
        // Insert it into a div with the ID "calendar".
        $("#calendar").html(data);
        checkIfElementExists(dateStr);
      },
      error: function (jqXHR, textStatus, errorThrown) {
        // An error occurred. Handle it here.
        console.error("Error: " + textStatus, errorThrown);
      },
    });
  }

  //check if prev and next buttons exist before adding event listeners
  function checkIfElementExists(dateStr) {
    console.log(dateStr);
    if ($(".prev").length > 0) {
      console.log('Element with class "prev" exists.');
      document.querySelector(".prev").addEventListener("click", function () {
        //On click of the previous button, get the previous month
        var prevDate = dateStr;
        console.log(prevDate);
        fetchCalendar(subtractOneMonth(prevDate), doctor_id);
      });
    } else {
      // The element does not exist
      console.log('Element with class "prev" does not exist.');
    }

    if ($(".next").length > 0) {
      console.log('Element with class "next" exists.');
      document.querySelector(".next").addEventListener("click", function () {
        //On click of the next button, get the next month
        console.log("Next button clicked");
        var nextDate = dateStr;
        console.log(nextDate);
        fetchCalendar(addOneMonth(nextDate), doctor_id);
      });

      // Select all td elements
      var tds = document.getElementsByTagName("td");

      // Add an event listener to each td
      for (var i = 0; i < tds.length; i++) {
        tds[i].addEventListener("click", function (event) {
          // Check if the td contains a span with the class dayAvailable
          if (this.getElementsByClassName("dayAvailable").length === 0) {
            // Check if the td's content is a number
            var content = this.textContent;
            var day = parseInt(content);
            if (!isNaN(day) && day >= 1 && day <= 31) {
              // Add a span with the class daySelected around the td's content
              this.innerHTML =
                '<span class="daySelected">' + content + "</span>";
            }
          }
        });
      }

      // Select all elements with the class daySelected
      var selectedDays = document.getElementsByClassName("daySelected");

      // Add a click event listener to each element
      for (var i = 0; i < selectedDays.length; i++) {
        selectedDays[i].addEventListener("click", function () {
          var content = this.textContent;
          console.log(content);
        });
      }
    } else {
      // The element does not exist
      console.log('Element with class "next" does not exist.');
    }
  }

  function subtractOneMonth(dateStr) {
    // Create a Date object from the date string
    var date = new Date(dateStr);

    // Subtract one month
    date.setMonth(date.getMonth() - 1);

    // Get the year and the month
    var year = date.getFullYear();
    var month = date.getMonth() + 1; // JavaScript counts months from 0 to 11

    // Pad the month with a leading zero if necessary
    if (month < 10) {
      month = "0" + month;
    }

    // Return the new date string
    return year + "-" + month;
  }

  function addOneMonth(dateStr) {
    // Create a Date object from the date string
    var date = new Date(dateStr);

    // Add one month
    date.setMonth(date.getMonth() + 1);

    // Get the year and the month
    var year = date.getFullYear();
    var month = date.getMonth() + 1; // JavaScript counts months from 0 to 11

    // Pad the month with a leading zero if necessary
    if (month < 10) {
      month = "0" + month;
    }

    // Return the new date string
    return year + "-" + month;
  }
});
