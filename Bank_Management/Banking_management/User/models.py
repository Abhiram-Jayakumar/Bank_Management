import random
from django.db import models
from django.utils import timezone

# Create your models here.
from django.db import models


class User(models.Model):
    ACCOUNT_TYPE_CHOICES = (
        ('salary', 'Salary Account'),
        ('student', 'Student Account'),
        ('savings', 'Savings Account'),
        ('current', 'Current Account'),
        ('joint', 'Joint Account'),
    )
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.CharField(max_length=255)
    account_number = models.CharField(max_length=20, unique=True, blank=True)
    password = models.CharField(max_length=128)  
    date_joined = models.DateTimeField(default=timezone.now)
    Adhaar = models.CharField(max_length=16, unique=True)
    Pan = models.CharField(max_length=15, unique=True)
    vstatus=models.IntegerField(default=0)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES, default='savings')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    

    def save(self, *args, **kwargs):
        if not self.account_number:
            self.account_number = self.generate_account_number()
        super(User, self).save(*args, **kwargs)

    def generate_account_number(self):
        account_number = str(random.randint(1000000000, 9999999999))
        while User.objects.filter(account_number=account_number).exists():
            account_number = str(random.randint(1000000000, 9999999999))
        return account_number



class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link transaction to a user
    transaction_type = models.CharField(max_length=6, choices=TRANSACTION_TYPE_CHOICES)  # Credit or Debit
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Transaction amount
    balance_amount = models.DecimalField(max_digits=10, decimal_places=2)  # User's balance after the transaction
    debit_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Optional debit amount
    credit_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Optional credit amount
    timestamp = models.DateTimeField(default=timezone.now)
    recipient = models.ForeignKey(User, related_name='received_transactions', on_delete=models.CASCADE)  # Recipient
    
    
class Complaint(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints')  # Link to the user
    title = models.CharField(max_length=255)  # Title of the complaint
    description = models.TextField()  # Detailed description of the complaint
    created_at = models.DateTimeField(default=timezone.now)  # Date and time of complaint creation
    status = models.CharField(max_length=10, default='unresolved')   # Current status of the complaint
    response = models.TextField(blank=True, null=True)  # Admin's response to the complaint
    responded_at = models.DateTimeField(blank=True, null=True) 