$(document).ready(function() {
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
    
    //Get doctor's planning
    var doctor_id = $('#doctor_id').val();

    $("form select[name='doctor']").change(function(){
        doctor_id = $(this).val();
        console.log(doctor_id);
        if(doctor_id != ''){
            $.ajax({
                type: "GET",
                url: '/get-doctorsProfile/' + doctor_id + '/',
                headers: {'X-CSRFToken': csrftoken}, 
                success: function(response){
                    console.log(response);
                    $('p[name="docteur_service"]').text(response.serviceName);
                    $('p[name="doctor_speciality"]').text(response.doctorProfile[0].speciality);
                    $('p[name="doctor_matricule"]').text(response.doctorProfile[0].matricule);
                    $('p[name="doctor_email"]').text(response.doctorMail);
                }
            });
        }
    });
});