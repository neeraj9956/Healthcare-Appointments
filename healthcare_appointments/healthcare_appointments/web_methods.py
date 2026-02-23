import frappe
from frappe.utils import get_datetime, add_to_date, today
from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry


@frappe.whitelist(allow_guest=True)
def book_appointment(data):

    data = frappe.parse_json(data)

    # 🔹 Get Service Doc (IMPORTANT)
    service_doc = frappe.get_doc("Healthcare Service", data.get("service"))

    duration = service_doc.duration_minutes
    price = service_doc.price

    # 🔹 Convert date + time into datetime
    start_datetime = get_datetime(
        f"{data.get('appointment_date')} {data.get('appointment_time')}"
    )

    # 🔹 Calculate End Time
    end_datetime = add_to_date(
        start_datetime,
        minutes=duration
    )

    end_time = end_datetime.time()

    # 🔹 Create Appointment
    appointment = frappe.get_doc({
        "doctype": "Patient Appointments",
        "patient_name": data.get("patient_name"),
        "patient_contact": data.get("patient_contact"),
        "appointment_date": data.get("appointment_date"),
        "appointment_time": data.get("appointment_time"),
        "service": data.get("service"),
        "gender": data.get("gender"),
        "end_time": end_time
    })

    appointment.insert(ignore_permissions=True)

    si = frappe.new_doc("Sales Invoice")
    si.customer = data.get("patient_name")
    si.posting_date = today()
    si.company = "Healthcare"

    si.append("items", {
        "item_code": service_doc.name,
        "qty": 1,
        "rate": price
    })

    si.insert(ignore_permissions=True)
    si.submit()
    pe = get_payment_entry("Sales Invoice", si.name)
    pe.mode_of_payment = "Cash"
    pe.company = "Healthcare"
    pe.insert(ignore_permissions=True)
    pe.submit()

    appointment.sales_invoice = si.name
    appointment.save(ignore_permissions=True)

    return "Appointment Booked & Paid Successfully"