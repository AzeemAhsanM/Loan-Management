from django import forms
from .models import Borrower, Loan, Repayment   

class BorrowerForm(forms.ModelForm):
    class Meta:
        model = Borrower
        fields = ['name', 'account_no', 'is_active']

class LoanForm(forms.ModelForm):
    class Meta:
        model  = Loan
        fields = ['borrower', 'amount', 'months']

class RepaymentForm(forms.ModelForm):
    class Meta:
        model = Repayment
        fields = ['loan', 'amount']