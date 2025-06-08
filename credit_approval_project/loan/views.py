from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Customer, Loan
from .serializers import CustomerSerializer
import math
from datetime import date

class RegisterCustomerView(APIView):
    def post(self, request):
        data = request.data.copy()
        try:
            salary = int(data.get("monthly_income"))
            approved_limit = round((36 * salary) / 100000) * 100000
            data["monthly_salary"] = salary
            data["approved_limit"] = approved_limit
            data["current_debt"] = 0.0

            serializer = CustomerSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    "customer_id": serializer.data["customer_id"],
                    "name": f"{serializer.data['first_name']} {serializer.data['last_name']}",
                    "age": data.get("age"),
                    "monthly_income": salary,
                    "approved_limit": approved_limit,
                    "phone_number": data.get("phone_number"),
                }
                return Response(response, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CheckEligibilityView(APIView):
    def post(self, request):
        try:
            data = request.data
            customer_id = data["customer_id"]
            loan_amount = float(data["loan_amount"])
            interest_rate = float(data["interest_rate"])
            tenure = int(data["tenure"])

            customer = Customer.objects.get(customer_id=customer_id)
            past_loans = Loan.objects.filter(customer=customer)

            score = 100

            if customer.current_debt > customer.approved_limit:
                score = 0
            else:
                total_loans = past_loans.count()
                total_volume = sum([loan.loan_amount for loan in past_loans])
                paid_on_time = sum([loan.emis_paid_on_time for loan in past_loans])

                if total_loans > 0:
                    score -= (total_loans - paid_on_time) * 5
                    score -= past_loans.filter(start_date__year=date.today().year).count() * 2
                    score += min(total_volume / 100000, 10)

            credit_score = max(0, min(score, 100))

            approval = False
            corrected_interest_rate = interest_rate

            if credit_score > 50:
                approval = True
            elif credit_score > 30:
                approval = True
                if interest_rate <= 12:
                    corrected_interest_rate = 16
            elif credit_score > 10:
                approval = True
                if interest_rate <= 16:
                    corrected_interest_rate = 20
            else:
                approval = False

            
            monthly_interest = corrected_interest_rate / (12 * 100)
            emi = (loan_amount * monthly_interest * (1 + monthly_interest) ** tenure) / \
                  ((1 + monthly_interest) ** tenure - 1)

            if emi * tenure > 0.5 * customer.monthly_salary * tenure:
                approval = False

            return Response({
                "customer_id": customer_id,
                "approval": approval,
                "interest_rate": interest_rate,
                "corrected_interest_rate": corrected_interest_rate,
                "tenure": tenure,
                "monthly_installment": round(emi, 2)
            })

        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        

class CreateLoanView(APIView):
    def post(self, request):
        try:
            data = request.data
            customer_id = data["customer_id"]
            loan_amount = float(data["loan_amount"])
            interest_rate = float(data["interest_rate"])
            tenure = int(data["tenure"])

            customer = Customer.objects.get(customer_id=customer_id)
            past_loans = Loan.objects.filter(customer=customer)

            score = 100
            if customer.current_debt > customer.approved_limit:
                score = 0
            else:
                total_loans = past_loans.count()
                total_volume = sum([loan.loan_amount for loan in past_loans])
                paid_on_time = sum([loan.emis_paid_on_time for loan in past_loans])

                if total_loans > 0:
                    score -= (total_loans - paid_on_time) * 5
                    score -= past_loans.filter(start_date__year=date.today().year).count() * 2
                    score += min(total_volume / 100000, 10)

            credit_score = max(0, min(score, 100))

            corrected_interest_rate = interest_rate
            approval = False

            if credit_score > 50:
                approval = True
            elif credit_score > 30:
                approval = True
                if interest_rate <= 12:
                    corrected_interest_rate = 16
            elif credit_score > 10:
                approval = True
                if interest_rate <= 16:
                    corrected_interest_rate = 20
            else:
                approval = False

           
            monthly_interest = corrected_interest_rate / (12 * 100)
            emi = (loan_amount * monthly_interest * (1 + monthly_interest) ** tenure) / \
                  ((1 + monthly_interest) ** tenure - 1)

            if emi * tenure > 0.5 * customer.monthly_salary * tenure:
                approval = False

            if not approval:
                return Response({
                    "loan_id": None,
                    "customer_id": customer_id,
                    "loan_approved": False,
                    "message": "Loan not approved due to eligibility criteria.",
                    "monthly_installment": round(emi, 2)
                }, status=200)

           
            today = date.today()
            end_date = date(today.year + (tenure // 12), today.month + (tenure % 12), today.day)

            loan = Loan.objects.create(
                customer=customer,
                loan_amount=loan_amount,
                tenure=tenure,
                interest_rate=corrected_interest_rate,
                monthly_installment=round(emi, 2),
                start_date=today,
                end_date=end_date,
                emis_paid_on_time=0
            )

           
            customer.current_debt += loan_amount
            customer.save()

            return Response({
                "loan_id": loan.loan_id,
                "customer_id": customer_id,
                "loan_approved": True,
                "message": "Loan approved and created successfully.",
                "monthly_installment": round(emi, 2)
            }, status=201)

        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


from .serializers import LoanSerializer

class ViewLoanView(APIView):
    def get(self, request, loan_id):
        try:
            loan = Loan.objects.get(loan_id=loan_id)
            customer = loan.customer

            return Response({
                "loan_id": loan.loan_id,
                "customer": {
                    "id": customer.customer_id,
                    "first_name": customer.first_name,
                    "last_name": customer.last_name,
                    "phone_number": customer.phone_number,
                    "age": customer.age
                },
                "loan_amount": loan.loan_amount,
                "interest_rate": loan.interest_rate,
                "monthly_installment": loan.monthly_installment,
                "tenure": loan.tenure
            }, status=200)

        except Loan.DoesNotExist:
            return Response({"error": "Loan not found"}, status=404)
        

class CustomerLoansView(APIView):
    def get(self, request, customer_id):
        try:
            customer = Customer.objects.get(customer_id=customer_id)
            loans = Loan.objects.filter(customer=customer)

            loan_list = []
            for loan in loans:
                repayments_left = loan.tenure - loan.emis_paid_on_time
                loan_list.append({
                    "loan_id": loan.loan_id,
                    "loan_amount": loan.loan_amount,
                    "interest_rate": loan.interest_rate,
                    "monthly_installment": loan.monthly_installment,
                    "repayments_left": repayments_left
                })

            return Response(loan_list, status=200)

        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=404)


