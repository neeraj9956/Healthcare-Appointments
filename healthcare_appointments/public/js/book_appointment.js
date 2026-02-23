$(document).ready(function(){
    load_services();

    $("#service, #time").on("change", function(){
        calculate_details();
    });

});

function load_services(){

    frappe.call({
        method:"healthcare_appointments.healthcare_appointments.api.get_services",
        callback: function (r) {
            if (r.message) {
                r.message.forEach(service => {
                    $("#service").append(
                        `<option value="${service.name}">
                            ${service.name}
                        </option>`
                    );

                });

            }
        }
    });

}


function calculate_details(){

    let service = $("#service").val();
    let time = $("#time").val();
    frappe.call({
        method:"healthcare_appointments.healthcare_appointments.api.calculate_appointment_details_for_guest",
        args:{
            service: service,
            appointment_time: time
        },
        callback:function(r){
            if(r.message){
                $("#end").text(r.message.end_time);
                $("#amount").text(r.message.price);
            }
        }
    });
}


function submit_booking(){

    let data = {
        patient_name: $("#patient_name").val(),
        patient_contact: $("#contact").val(),
        appointment_date: $("#date").val(),
        appointment_time: $("#time").val(),
        service: $("#service").val(),
        gender:$("#gender").val()
    };


    frappe.call({
        method:"healthcare_appointments.healthcare_appointments.web_methods.book_appointment",
        args:{
            data: data
        },
        callback:function(r){

            frappe.msgprint(r.message);
        }
    });

}