from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse

from .models import Borrower, Loan, Repayment

# Borrower Views
from .form import BorrowerForm, LoanForm, RepaymentForm
def borrower_list(request):
    q = Borrower.objects.all().order_by('name')
    return render(request, 'myapp/borrower_list.html', {'borrowers': q})

def borrower_create(request):
    form = BorrowerForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('borrower_list')
    return render(request, 'myapp/form.html', {'form': form, 'title': 'Create Borrower'})

def borrower_edit(request, pk):
    obj = get_object_or_404(Borrower, pk=pk)
    form = BorrowerForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('borrower_list')
    return render(request, 'myapp/form.html', {'form': form, 'title': 'Edit Borrower'})

# Loan Views

def loan_create(request):
    form = LoanForm(request.POST or None)
    if form.is_valid():
        loan = form.save(commit=False)
        loan.status = 'PENDING'
        loan.save()
        messages.success(request, f"Loan {loan.loan_id} created (Pending).")
        return redirect('borrower_list')    
    return render(request, 'myapp/form.html', {'form': form, 'title': 'Create Loan'})

def loan_details(request, loan_id):
    