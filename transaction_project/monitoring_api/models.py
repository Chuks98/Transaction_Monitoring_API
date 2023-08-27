from django.db import models

TIER_CHOICES = (1, 2)

class Transaction(models.Model):
    user = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tier_number = models.IntegerField(choices=TIER_CHOICES, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    flagged = models.BooleanField(default=False)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.amount}"

