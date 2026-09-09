from django.db import models



class Country(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    code = models.CharField(
        max_length=10,
        unique=True
    )

    def __str__(self):
        return self.name
    
    
    
class City(models.Model):

    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name='cities'
    )

    name = models.CharField(
        max_length=100
    )

    def __str__(self):
        return f"{self.name} - {self.country.name}"
    
    
    
    
    
class Accommodation(models.Model):

    ACCOMMODATION_TYPES = (
        ('hotel', 'هتل'),
        ('eco_lodge', 'بوم‌گردی'),
        ('villa', 'ویلا'),
        ('suite', 'سوئیت'),
        ('hostel', 'هاستل'),
        ('camp', 'کمپ'),
        ('local_house', 'خانه محلی'),
        ('other', 'سایر'),
    )

    name = models.CharField(
        max_length=200
    )

    type = models.CharField(
        max_length=20,
        choices=ACCOMMODATION_TYPES
    )

    city = models.ForeignKey(
        'City',
        on_delete=models.PROTECT
    )

    address = models.TextField(
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.name} - {self.city}"


class Tour(models.Model):

    STATUS_CHOICES = (
        ('open', 'در حال ثبت نام'),
        ('full', 'تکمیل ظرفیت'),
        ('running', 'در حال اجرا'),
        ('finished', 'پایان یافته'),
        ('cancelled', 'لغو شده'),
    )

    title = models.CharField(
        max_length=200,
        verbose_name='عنوان تور'
    )

    tour_code = models.CharField(
        max_length=30,
        unique=True,
        blank=True,
        verbose_name='کد تور'
    )

    destination = models.CharField(
        max_length=100,
        verbose_name='مقصد'
    )
    
    destination_city = models.ForeignKey(
        City,
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    departure_date = models.DateField(
        verbose_name='تاریخ حرکت'
    )

    return_date = models.DateField(
        verbose_name='تاریخ برگشت'
    )

    capacity = models.PositiveIntegerField(
        verbose_name='ظرفیت'
    )

    adult_price = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        verbose_name='قیمت بزرگسال'
    )

    child_price = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        blank=True,
        null=True,
        verbose_name='قیمت کودک'
    )

    services = models.TextField(
        blank=True,
        null=True,
        verbose_name='خدمات تور'
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='توضیحات'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='open',
        verbose_name='وضعیت'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):

        if not self.tour_code:

            last_tour = Tour.objects.order_by('-id').first()

            next_number = 1

            if last_tour and last_tour.tour_code:
                next_number = int(
                    last_tour.tour_code.split('-')[-1]
                ) + 1

            self.tour_code = f"TOUR-{next_number:05d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tour_code} - {self.title}"
    
    

class TourAccommodation(models.Model):

    tour = models.ForeignKey(
        'Tour',
        on_delete=models.CASCADE,
        related_name='accommodations'
    )

    accommodation = models.ForeignKey(
        'Accommodation',
        on_delete=models.PROTECT
    )

    check_in_date = models.DateField(
        blank=True,
        null=True
    )

    check_out_date = models.DateField(
        blank=True,
        null=True
    )

    nights = models.PositiveIntegerField(
        default=1
    )

    order = models.PositiveIntegerField(
        default=1
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.tour} - {self.accommodation} ({self.nights} nights)"






class Flight(models.Model):

    TRANSPORT_TYPES = (
        ('flight', 'پرواز'),
        ('train', 'قطار'),
        ('bus', 'اتوبوس'),
        ('transfer', 'ترانسفر'),
    )

    transport_type = models.CharField(
        max_length=20,
        choices=TRANSPORT_TYPES,
        default='flight'
    )

    from_city = models.ForeignKey(
        'City',
        on_delete=models.PROTECT,
        related_name='flights_from'
    )

    to_city = models.ForeignKey(
        'City',
        on_delete=models.PROTECT,
        related_name='flights_to'
    )

    airline = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    flight_number = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    departure_time = models.DateTimeField(
        blank=True,
        null=True
    )

    arrival_time = models.DateTimeField(
        blank=True,
        null=True
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        blank=True,
        null=True
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.from_city} → {self.to_city}"
    
    
    
    
    
class Visa(models.Model):

    country = models.ForeignKey(
        Country,
        on_delete=models.PROTECT
    )

    visa_type = models.CharField(
        max_length=100
    )

    processing_days = models.PositiveIntegerField(
        default=0
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        default=0
    )

    notes = models.TextField(
        blank=True,
        null=True
    )
    
    validity_days = models.PositiveIntegerField(
    default=30
    )

    def __str__(self):
        return f"{self.country} - {self.visa_type}"
    
    
    
        
    
    
class TourFlight(models.Model):

    tour = models.ForeignKey(
        'Tour',
        on_delete=models.CASCADE,
        related_name='flights'
    )

    flight = models.ForeignKey(
        'Flight',
        on_delete=models.PROTECT
    )

    order = models.PositiveIntegerField(
        default=1
    )

    date = models.DateField(
        blank=True,
        null=True
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.tour} - {self.flight}"
    
    
    
    
