from decimal import Decimal
from django.db import models
from django.utils import timezone

# Create your models here.

class Borrower(models.Model):
    name = models.CharField(max_length=100)
    account_no = models.CharField(max_length=12,unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True) 

    # simple running balance for approved loans – repayments reduce this
    current_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name} ({self.account_no})"

# to generate Loan Id
def loan_id():
    last = Loan.objects.order_by("-created_at").first()
    if not last or not last.loan_id:
        n = 1
    else:
        n = int(last.loan_id.replace("LN", "")) + 1
    return f"LN{n:05d}"

#receipt gener
def receipt_no():
    #timestamp based unique receipt number
    return f"LR-{timezone.now().strftime('%y%m%d%H%M%S%f')[:12]}"    

class Loan(models.Model):
    Loan_Status = [
        ('PENDING', 'Pending'), 
        ('APPROVED', 'Approved'), 
        ('REJECTED', 'Rejected'),
        ('REPAID', 'Repaid')
        ]
    loan_id = models.CharField(max_length=10, unique=True, editable=False, default=loan_id)
    Borrower = models.ForeignKey(Borrower, on_delete=models.PROTECT, related_name='loans')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    months = models.PositiveIntegerField(default=12)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=Loan_Status, default='PENDING')

    def save(self, *args, **kwargs):
        if not self.loan_id:
            self.loan_id = loan_id()
        super().save(*args, **kwargs)

    @property
    def total_paid(self):
        agg = self.Repayments.aggregate(total = models.Sum('amount')) 
        return agg['total'] or Decimal('0.00')

    @property
    def balance(self):
        return (self.amount - self.total_paid).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def __str__(self):
        return f"{self.loan_id} - {self.borrower.name}"
