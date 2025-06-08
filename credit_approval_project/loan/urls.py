from django.urls import path
from . import views

urlpatterns = [
    path('register', views.RegisterCustomerView.as_view(), name='register-customer'),
    path('check-eligibility', views.CheckEligibilityView.as_view(), name='check-eligibility'),
    path('create-loan', views.CreateLoanView.as_view(), name='create-loan'),
    path('view-loan/<int:loan_id>', views.ViewLoanView.as_view(), name='view-loan'),
    path('view-loans/<int:customer_id>', views.CustomerLoansView.as_view(), name='view-loans'),
]
