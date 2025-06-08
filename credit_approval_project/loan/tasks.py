from celery import shared_task
import pandas as pd
from .models import Customer, Loan

@shared_task
def ingest_customer_data_from_excel(file_path):
    df = pd.read_excel(file_path)
    for _, row in df.iterrows():
        Customer.objects.update_or_create(
            customer_id=row['Customer ID'], 
            defaults={
                'first_name': row['First Name'],
                'last_name': row['Last Name'],
                'age': row['Age'],
                'phone_number': row['Phone Number'],
                'monthly_salary': row['Monthly Salary'],
                'approved_limit': row['Approved Limit'],
            }
        )

@shared_task
def ingest_loan_data_from_excel(file_path):
    df = pd.read_excel(file_path)
    for _, row in df.iterrows():
        Loan.objects.update_or_create(
            loan_id=row['Loan ID'],
            defaults={
                'customer_id': row['Customer ID'],
                'loan_amount': row['Loan Amount'],
                'tenure': row['Tenure'],
                'interest_rate': row['Interest Rate'],
                'monthly_repayment': row['Monthly payment'],
                'emis_paid_on_time': row['EMIs paid on Time'],
                'start_date': pd.to_datetime(row['Date of Approval']),
                'end_date': pd.to_datetime(row['End Date']),
            }
        )
