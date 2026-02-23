import frappe
from datetime import datetime, timedelta

@frappe.whitelist()
def calculate_appointment_details(service, appointment_time):
    duration, price = frappe.get_value("Healthcare Service",service,["duration_minutes", "price"])
    start = datetime.strptime(appointment_time, "%H:%M:%S")
    end = start + timedelta(minutes=duration)
    return {"end_time": end.time(),"price": price}

@frappe.whitelist(allow_guest=True)
def get_services():
    return frappe.get_all(
        "Healthcare Service",
        fields=["name"]
    )
    
import frappe
from datetime import datetime, timedelta


@frappe.whitelist(allow_guest=True)
def calculate_appointment_details_for_guest(service, appointment_time):

    # 🛑 Prevent crash if empty
    if not appointment_time:
        return {}

    duration, price = frappe.get_value(
        "Healthcare Service",
        service,
        ["duration_minutes", "price"]
    )

    # ✅ Browser sends HH:MM
    start = datetime.strptime(appointment_time, "%H:%M")

    end = start + timedelta(minutes=duration)

    return {
        "end_time": end.strftime("%H:%M"),
        "price": price
    }
