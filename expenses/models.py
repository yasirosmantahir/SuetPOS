from datetime import date

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class ExpenseType(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateField(default=date.today)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.name)


class Expense(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    expense_type = models.ForeignKey(ExpenseType, on_delete=models.DO_NOTHING)
    paid_amount = models.DecimalField(default=0, decimal_places=2, max_digits=20)
    cheque_num = models.CharField(max_length=30, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateField(default=date.today)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.name)

    class Meta:
        permissions = [
            ("void_expense", "Can void expense"),
        ]

