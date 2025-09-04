from django.db import models

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
