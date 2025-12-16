from django.db import models
from django.utils import timezone

class Expense(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'expense'
    
    def __str__(self):
        return f"Expense: {self.amount} - {self.note}"

class Income(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'income'

    def __str__(self):
        return f"Income: {self.amount} - {self.note}"
