// Copyright (c) 2026, Neeraj Ravi Pratap and contributors
// For license information, please see license.txt

frappe.ui.form.on("Patient Appointments", {
    refresh(frm) {
        if(frm.doc.status){
            frm.page.set_indicator(frm.doc.status, get_color(frm.doc.status));
        }

    },
    on_submit(frm) {
        frm.set_value("status", "Completed");
        
    },
    on_cancel(frm) {
        frm.set_value("status", "Cancelled");
    },
     service: function(frm) {
        calculate_details(frm);
    },

    appointment_time: function(frm) {
        calculate_details(frm);
    }
});
function calculate_details(frm) {

    if(frm.doc.service && frm.doc.appointment_time){

        frappe.call({
            method: "healthcare_appointments.healthcare_appointments.api.calculate_appointment_details",
            args:{
                service: frm.doc.service,
                appointment_time: frm.doc.appointment_time
            },
            callback:function(r){
                if(r.message){
                    frm.set_value("estimated_end_time", r.message.end_time);
                    frm.set_value("total_amount", r.message.price);
                }
            }
        });

    }
}
function get_color(status) {

    if (status === "Scheduled") {
        return "blue";
    }

    if (status === "Completed") {
        return "green";
    }

    if (status === "Cancelled") {
        return "red";
    }
}
