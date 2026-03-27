from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    ROLE_CHOICES = [
        ('tenant', 'Tenant – I want to rent'),
        ('agent',  'Agent / Landlord – I have properties'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='tenant')

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class Property(models.Model):

    TYPE_CHOICES = [
        ('apartment', 'Apartment / Flat'),
        ('duplex',    'Duplex'),
        ('bungalow',  'Bungalow'),
        ('selfcon',   'Self-contained'),
        ('shortlet',  'Short Let'),
        ('land',      'Land'),
    ]

    LISTING_CHOICES = [
        ('rent',     'For Rent'),
        ('sale',     'For Sale'),
        ('shortlet', 'Short Let'),
    ]

    STATUS_CHOICES = [
        ('active',   'Active'),
        ('pending',  'Pending Review'),
        ('inactive', 'Inactive'),
    ]

    LOCATION_CHOICES = [
        ('Lekki Phase 1',    'Lekki Phase 1'),
        ('Lekki Phase 2',    'Lekki Phase 2'),
        ('Ikoyi',            'Ikoyi'),
        ('Victoria Island',  'Victoria Island'),
        ('Surulere',         'Surulere'),
        ('Ikeja',            'Ikeja'),
        ('Ajah',             'Ajah'),
        ('Yaba',             'Yaba'),
        ('Gbagada',          'Gbagada'),
        ('Magodo',           'Magodo'),
        ('Festac',           'Festac'),
        ('Isale Eko',        'Isale Eko'),
    ]

    # Core fields
    owner        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    title        = models.CharField(max_length=200)
    description  = models.TextField()
    property_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    listing_type  = models.CharField(max_length=20, choices=LISTING_CHOICES, default='rent')
    status        = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Location
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES)
    address  = models.CharField(max_length=255, blank=True)

    # Details
    price     = models.PositiveIntegerField(help_text='Annual rent or sale price in Naira')
    bedrooms  = models.PositiveSmallIntegerField(default=1)
    bathrooms = models.PositiveSmallIntegerField(default=1)
    toilets   = models.PositiveSmallIntegerField(default=1)
    size      = models.PositiveIntegerField(blank=True, null=True, help_text='Size in m²')

    # Amenities
    has_water     = models.BooleanField(default=False)
    has_generator = models.BooleanField(default=False)
    has_security  = models.BooleanField(default=False)
    has_parking   = models.BooleanField(default=False)
    has_cctv      = models.BooleanField(default=False)
    has_bq        = models.BooleanField(default=False)
    has_kitchen   = models.BooleanField(default=False)
    has_wardrobe  = models.BooleanField(default=False)
    has_ac        = models.BooleanField(default=False)
    has_pool      = models.BooleanField(default=False)
    has_gym       = models.BooleanField(default=False)
    has_internet  = models.BooleanField(default=False)

    # Contact
    phone        = models.CharField(max_length=20)
    whatsapp     = models.CharField(max_length=20, blank=True)
    availability = models.CharField(max_length=200, blank=True)

    # Media
    image = models.ImageField(upload_to='properties/', blank=True, null=True)

    # Stats
    views = models.PositiveIntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Properties'

    def __str__(self):
        return f"{self.title} – {self.location}"


class SavedProperty(models.Model):
    user     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_properties')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'property')

    def __str__(self):
        return f"{self.user.username} saved {self.property.title}"
class ContactMessage(models.Model):
    full_name   = models.CharField(max_length=100)
    email       = models.EmailField()
    phone       = models.CharField(max_length=20, blank=True)
    subject     = models.CharField(max_length=200)
    message     = models.TextField()
    is_read     = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} – {self.subject}"