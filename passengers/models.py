from django.db import models
from django.db.models import Max
from datetime import date


class Passenger(models.Model):

    customer_code = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    national_code = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    birth_date = models.DateField(
        blank=True,
        null=True
    )

    phone = models.CharField(max_length=20)

    email = models.EmailField(
        blank=True,
        null=True
    )

    address = models.TextField(
        blank=True,
        null=True
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
    
    
    def save(self, *args, **kwargs):

        if not self.customer_code:

            last_passenger = Passenger.objects.order_by('-id').first()

            if last_passenger:
                last_number = int(
                    last_passenger.customer_code.split('-')[1]
                )
                next_number = last_number + 1
            else:
                next_number = 1

            self.customer_code = f"TRV-{next_number:05d}"

        super().save(*args, **kwargs)
        

    def __str__(self):
        return f"{self.customer_code} - {self.first_name} {self.last_name}"
    
    
#----------------------------------------------------------#    
    
class Passport(models.Model):

    passenger = models.OneToOneField(
        Passenger,
        on_delete=models.CASCADE,
        related_name='passport'
    )

    passport_number = models.CharField(
        max_length=50,
        unique=True
    )

    issue_date = models.DateField()

    expiry_date = models.DateField()

    country = models.CharField(
        max_length=100,
        default='Iran'
    )

        
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    
    
    def __str__(self):
        return self.passport_number    
    
    @property
    def days_to_expire(self):

        return (
            self.expiry_date
            - date.today()
        ).days
        
        
    @property
    def is_expiring_soon(self):

        return self.days_to_expire <= 180
    
    
    
#-------------------------------------------------------------#
    
class Document(models.Model):
    
    DOCUMENT_TYPES = (
    ('passport_image', 'تصویر پاسپورت'),
    ('visa', 'ویزا'),
    ('national_card', 'کارت ملی'),
    ('personal_photo', 'عکس پرسنلی'),
    ('ticket', 'بلیت'),
    ('insurance', 'بیمه'),
    ('other', 'سایر'),
)

   

    passenger = models.ForeignKey(
        Passenger,
        on_delete=models.CASCADE,
        related_name='documents'
    )

    title = models.CharField(
        max_length=200
    )

    document_type = models.CharField(
        max_length=30,
        choices=DOCUMENT_TYPES
    )

    file = models.FileField(
        upload_to='documents/'
    )
    
    expiry_date = models.DateField(
    blank=True,
    null=True
    )

    notes = models.TextField(
    blank=True,
    null=True
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title
    
    
    @property
    def days_to_expire(self):

        if not self.expiry_date:
            return None

        return (
            self.expiry_date
            - date.today()
        ).days
        
        
    @property
    def is_image(self):

        image_extensions = (
            '.jpg',
            '.jpeg',
            '.png',
            '.webp'
        )

        return self.file.name.lower().endswith(
            image_extensions
        )