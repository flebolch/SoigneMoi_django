
window.onload = function() {
    // Get the current date
    var date = new Date();

    // Get the year and the month
    var year = date.getFullYear();
    var month = date.getMonth() + 1; // getMonth() returns the month number from 0 to 11

    // Format the month as a two-digit number
    if (month < 10) {
        month = '0' + month;
    }

    // Combine the year and the month into a string in the "YYYY-MM" format
    var dateStr = year + '-' + month;

    $.ajax({
        url: "/selectedMonth/" + dateStr + "/",
        type: "GET",
        success: function(data) {
            // The server responded with the calendar in HTML format.
            // Insert it into a div with the ID "calendar".
            $('#calendar').html(data);
        },
        error: function(jqXHR, textStatus, errorThrown) {
            // An error occurred. Handle it here.
            console.error("Error: " + textStatus, errorThrown);
        }
    });

}



// //get the current date from the input
// var dateInput = document.getElementById('id_date');


// Get the elements for the month, year, and days
// var monthElement = document.querySelector('.month li');
// var yearElement = document.querySelector('.month span');
// var daysElement = document.querySelector('.days');

// Update the month and year
// monthElement.textContent = date.toLocaleString('default', { month: 'long' });
// yearElement.textContent = date.getFullYear();

// Update the days
// daysElement.innerHTML = '';
// for (var i = 1; i <= new Date(date.getFullYear(), date.getMonth()+1, 0).getDate(); i++) {
//     if (i === date.getDate()) {
//         // If the day is the current day, highlight it
//         daysElement.innerHTML += '<li><span class="active">' + i + '</span></li>';
//     } else {
//         daysElement.innerHTML += '<li>' + i + '</li>';
//     }
// }
  
// });
