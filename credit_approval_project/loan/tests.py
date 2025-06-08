from rest_framework.test import APITestCase
from django.urls import reverse
from loan.models import Customer 

class CreditApprovalTests(APITestCase):
    
    def setUp(self):
        self.register_url = reverse('register-customer')
        self.eligibility_url = reverse('check-eligibility')
        self.create_loan_url = reverse('create-loan')
    
    def test_register_customer(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "age": 30,
            "monthly_income": 50000,
            "phone_number": "1234567890"
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn("customer_id", response.data)
        self.assertEqual(response.data["approved_limit"], 1800000)  

    def test_check_eligibility_invalid_customer(self):
        data = {
            "customer_id": 9999,
            "loan_amount": 100000,
            "interest_rate": 14,
            "tenure": 12
        }
        response = self.client.post(self.eligibility_url, data, format='json')
        self.assertEqual(response.status_code, 404)

    def test_create_loan_invalid_customer(self):
        data = {
            "customer_id": 9999,
            "loan_amount": 100000,
            "interest_rate": 14,
            "tenure": 12
        }
        response = self.client.post(self.create_loan_url, data, format='json')
        self.assertEqual(response.status_code, 404)
