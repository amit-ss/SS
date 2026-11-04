from django.db import models

class CampusLocation(models.Model):
    CATEGORY_CHOICES = [
        ('academic', 'Academic Block'),
        ('lab', 'Computer / Science Lab'),
        ('hostel', 'Residential / Hostel'),
        ('cafeteria', 'Food Court & Cafeteria'),
        ('library', 'Central Library'),
        ('sports', 'Sports & Gymnasium'),
        ('office', 'Administrative Office'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='academic')
    block_number = models.CharField(max_length=50, help_text="e.g. Block 34, UniMall, Unipolis")
    floor_or_room = models.CharField(max_length=100, default="Ground Floor")
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.TextField()
    qr_code_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    image_url = models.CharField(max_length=300, blank=True, null=True)
    is_popular = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.block_number})"
