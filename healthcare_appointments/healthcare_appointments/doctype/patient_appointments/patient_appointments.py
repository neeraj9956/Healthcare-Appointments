# Copyright (c) 2026, Neeraj Ravi Pratap and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta, time
from frappe.utils import getdate, get_time


class PatientAppointments(Document):

    def before_save(self):
        self.validate_overlap()
        self.validate_working_hours()
    
    def after_insert(self):
        self.create_patient()
    
    
    def create_patient(self):
        existing_patient = frappe.db.exists( "Patient",{"mobile": self.patient_contact})
        if existing_patient:
            return

        patient = frappe.new_doc("Patient")
        patient.first_name = self.patient_name
        patient.mobile = self.patient_contact
        patient.email = self.patient_email
        patient.sex = self.gender
        patient.insert(ignore_permissions=True)

        self.patient = patient.name
        

    def validate_overlap(self):
        appointments = frappe.get_all("Patient Appointments",filters={"patient_contact": self.patient_contact,"appointment_date": self.appointment_date,
                                                                    "status": "Scheduled","name": ["!=", self.name]},fields=["appointment_time", "estimated_end_time"])
        self_date = getdate(self.appointment_date)
        start1 = datetime.combine(self_date, get_time(self.appointment_time))
        end1 = datetime.combine(self_date, get_time(self.estimated_end_time))
        for appt in appointments:
            start2 = datetime.combine(self_date, get_time(appt.appointment_time))
            end2 = datetime.combine(self_date, get_time(appt.estimated_end_time))
            if start1 < end2 and end1 > start2:
                frappe.throw("Appointment Overlap Detected!")
    def validate_working_hours(self):
        clinic_start = time(9, 0, 0)
        clinic_end   = time(17, 0, 0)

        start_time = self.appointment_time
        end_time   = self.estimated_end_time

        if isinstance(start_time, str):
            start_time = frappe.utils.get_time(start_time)

        if isinstance(end_time, str):
            end_time = frappe.utils.get_time(end_time)

        if start_time < clinic_start or end_time > clinic_end:
            frappe.throw("Appointment must be between 9 AM to 5 PM")
    
    def on_update(self):
        if self.status == "Completed":
            frappe.logger().info(f"Appointment {self.name} Completed")