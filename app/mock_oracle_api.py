# app/mock_oracle_api.py
# simulates Orale Fusion REST API endpoints with realistic enterprise data
from datetime import datetime, timedelta
import random
# ----MOCK DATABASE-----
EMPLOYEES = [
    {"id": "EMP001", "name": "Rajesh Kumar",    "department": "Finance",    "role": "Senior Accountant",  "salary": 85000,  "status": "Active",   "location": "Mumbai"},
    {"id": "EMP002", "name": "Priya Sharma",    "department": "HR",         "role": "HR Manager",          "salary": 92000,  "status": "Active",   "location": "Bangalore"},
    {"id": "EMP003", "name": "Amit Patel",      "department": "IT",         "role": "Software Engineer",   "salary": 95000,  "status": "Active",   "location": "Pune"},
    {"id": "EMP004", "name": "Sunita Verma",    "department": "Finance",    "role": "Finance Controller",  "salary": 110000, "status": "Active",   "location": "Delhi"},
    {"id": "EMP005", "name": "Rohit Mehta",     "department": "SCM",        "role": "Supply Chain Lead",   "salary": 88000,  "status": "Active",   "location": "Chennai"},
    {"id": "EMP006", "name": "Neha Gupta",      "department": "HR",         "role": "Recruiter",           "salary": 65000,  "status": "Active",   "location": "Bangalore"},
    {"id": "EMP007", "name": "Vikram Singh",    "department": "IT",         "role": "DevOps Engineer",     "salary": 98000,  "status": "Inactive", "location": "Hyderabad"},
    {"id": "EMP008", "name": "Anita Desai",     "department": "Finance",    "role": "Junior Accountant",   "salary": 55000,  "status": "Active",   "location": "Mumbai"},
]

PURCHASE_ORDERS = [
    {"id": "PO-2024-001", "vendor": "TechCorp Solutions",    "amount": 45000,  "status": "Open",     "department": "IT",      "date": "2024-01-15", "description": "Software licenses"},
    {"id": "PO-2024-002", "vendor": "Office Supplies Ltd",   "amount": 8500,   "status": "Approved", "department": "HR",      "date": "2024-01-20", "description": "Office furniture"},
    {"id": "PO-2024-003", "vendor": "CloudHost Inc",         "amount": 120000, "status": "Open",     "department": "IT",      "date": "2024-02-01", "description": "Cloud infrastructure"},
    {"id": "PO-2024-004", "vendor": "Raw Materials Co",      "amount": 75000,  "status": "Closed",   "department": "SCM",     "date": "2024-02-10", "description": "Manufacturing materials"},
    {"id": "PO-2024-005", "vendor": "Training Academy",      "amount": 25000,  "status": "Open",     "department": "HR",      "date": "2024-02-15", "description": "Employee training"},
    {"id": "PO-2024-006", "vendor": "Security Systems Ltd",  "amount": 35000,  "status": "Approved", "department": "IT",      "date": "2024-03-01", "description": "Security infrastructure"},
    {"id": "PO-2024-007", "vendor": "Logistics Partner",     "amount": 18000,  "status": "Open",     "department": "SCM",     "date": "2024-03-10", "description": "Shipping services"},
    {"id": "PO-2024-008", "vendor": "Consulting Group",      "amount": 95000,  "status": "Open",     "department": "Finance", "date": "2024-03-15", "description": "Financial consulting"},
]

INVOICES = [
    {"id": "INV-2024-001", "vendor": "TechCorp Solutions",   "amount": 45000,  "status": "Pending",  "due_date": "2024-04-15", "po_ref": "PO-2024-001"},
    {"id": "INV-2024-002", "vendor": "Office Supplies Ltd",  "amount": 8500,   "status": "Paid",     "due_date": "2024-03-20", "po_ref": "PO-2024-002"},
    {"id": "INV-2024-003", "vendor": "CloudHost Inc",        "amount": 120000, "status": "Overdue",  "due_date": "2024-03-01", "po_ref": "PO-2024-003"},
    {"id": "INV-2024-004", "vendor": "Raw Materials Co",     "amount": 75000,  "status": "Paid",     "due_date": "2024-03-10", "po_ref": "PO-2024-004"},
    {"id": "INV-2024-005", "vendor": "Training Academy",     "amount": 25000,  "status": "Pending",  "due_date": "2024-04-20", "po_ref": "PO-2024-005"},
    {"id": "INV-2024-006", "vendor": "Consulting Group",     "amount": 95000,  "status": "Overdue",  "due_date": "2024-03-01", "po_ref": "PO-2024-008"},
]
# ---- API FUNCTIONS ----

def get_employees(department: str=None, status: str= None) -> list:
    """Get employees with optional filters."""
    result=EMPLOYEES.copy()
    if department:
        result=[e for e in result if e["department"].lower()==department.lower()]
    if status:
        result=[e for e in result if e["status"].lower()==status.lower()]
    return result

def get_purchase_orders(status: str=None, department: str=None, min_amount: float =None) -> list:
    """Get purchase orders with optional filters."""
    result = PURCHASE_ORDERS.copy()
    if status:
        result=[po for po in result if po["status"].lower()==status.lower()]
    if department:
        result=[po for po in result if po["department"].lower()==department.lower()]
    if min_amount:
        result=[po for po in result if po["min_amount"] >= min_amount]
    return result

def get_invoices(status: str=None) -> list:
    """Get invoices with optional filters."""
    result = INVOICES.copy()
    if status:
        result=[inv for inv in result if inv["status"].lower()==status.lower()]
        return result

def get_department_summary() -> dict:
    """Get summary statistics by department."""
    departments= {}
    for emp in EMPLOYEES:
        dept=emp["department"]
        if dept not in departments:
            departments[dept]={"employee_count":0, "total_salary":0}
        departments[dept]["employee_count"]+=1
        departments[dept]["total_salary"]+= emp["salary"]
    for dept in departments:
        departments[dept]["avg_salary"]=(
            departments[dept]["total_salary"] // departments[dept]["employee_count"]
        )
    return departments            

