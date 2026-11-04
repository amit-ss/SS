from django.db import models
from django.contrib.auth.models import User

class LostFoundItem(models.Model):
    TYPE_CHOICES = [
        ('lost', 'Lost Item'),
        ('found', 'Found Item'),
    ]
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics & Laptops'),
        ('id_cards', 'Student ID & Wallets'),
        ('books', 'Books & Notebooks'),
        ('accessories', 'Watches & Earbuds'),
        ('keys', 'Room & Vehicle Keys'),
        ('other', 'Other Miscellaneous'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('claimed', 'Claimed'),
        ('returned', 'Returned to Owner'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='reported_items')
    reporter_name = models.CharField(max_length=100, default="LPU Student")
    item_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='lost')
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='electronics')
    description = models.TextField()
    location_name = models.CharField(max_length=200, help_text="e.g. Block 34 Lab 402, UniMall Food Court")
    date_time = models.DateTimeField(auto_now_add=True)
    photo = models.FileField(upload_to='lost_found/', null=True, blank=True)
    photo_url = models.CharField(max_length=300, blank=True, null=True)
    contact_phone = models.CharField(max_length=20, default="+91 9876543210")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_moderated = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date_time']

    def __str__(self):
        return f"[{self.item_type.upper()}] {self.title} @ {self.location_name}"

class ItemClaim(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Verification'),
        ('approved', 'Claim Approved'),
        ('rejected', 'Claim Rejected'),
    ]
    item = models.ForeignKey(LostFoundItem, on_delete=models.CASCADE, related_name='claims')
    claimant = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    claimant_name = models.CharField(max_length=100)
    claimant_phone = models.CharField(max_length=20)
    proof_description = models.TextField(help_text="Provide identifiable features such as serial numbers or stickers.")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Claim for {self.item.title} by {self.claimant_name}"
