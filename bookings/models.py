from django.db import models
from django.db.models import Sum
from payments.models import Payment
from passengers.models import Passenger

class Booking(models.Model):

    STATUS_CHOICES = (
        ('pending', 'در انتظار'),
        ('confirmed', 'تایید شده'),
        ('cancelled', 'لغو شده'),
        ('finished', 'پایان یافته'),
    )

    passenger = models.ForeignKey(
        'passengers.Passenger',
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    booking_code = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        default=0
    )
    

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):

        if not self.booking_code:

            last = Booking.objects.order_by('-id').first()

            next_number = 1
            if last and last.booking_code:
                next_number = int(last.booking_code.split('-')[-1]) + 1

            self.booking_code = f"BK-{next_number:05d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.booking_code} - {self.passenger}"
    
    
    

    @property
    def paid_amount(self):
        return self.payments.aggregate(
            total=Sum('amount')
        )['total'] or 0


    @property
    def remaining_amount(self):
        remaining = (
            (self.total_price or 0)
            - self.paid_amount
        )
        return max(0, remaining)
    
    
        
    @property
    def actual_total_price(self):

        total = 0

        for item in self.items.all():

            total += item.final_price

        return total
    

#--------------------------------------------------------------#  
    
class BookingItem(models.Model):

    ITEM_TYPE_CHOICES = (
        ('tour', 'تور'),
        ('flight', 'پرواز'),
        ('accommodation', 'اقامتگاه'),
        ('visa', 'ویزا'),
    )

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name='items'
    )

    item_type = models.CharField(
        max_length=20,
        choices=ITEM_TYPE_CHOICES
    )

    tour = models.ForeignKey(
        'tours.Tour',
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    flight = models.ForeignKey(
        'tours.Flight',
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    accommodation = models.ForeignKey(
        'tours.Accommodation',
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    
    
    visa = models.ForeignKey(
    'tours.Visa',
    on_delete=models.PROTECT,
    blank=True,
    null=True
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

    def __str__(self):
        return f"{self.booking} - {self.item_type}"
    
    
    @property
    def refunded_amount(self):

        return self.refunds.aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        
        
    @property
    def final_price(self):

        return (
            self.price -
            self.refunded_amount
        )
    
    


#-----------------------------------------------------------------------#

class BookingVisa(models.Model):

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name='visas'
    )

    visa = models.ForeignKey(
        'tours.Visa',
        on_delete=models.PROTECT
    )

    quantity = models.PositiveIntegerField(
        default=1
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

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.booking} - {self.visa}"
    
    
    
#-------------------------------------------------------#
class BookingFlight(models.Model):

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name='flights'
    )

    flight = models.ForeignKey(
        'tours.Flight',
        on_delete=models.PROTECT
    )

    quantity = models.PositiveIntegerField(
        default=1
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

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.booking} - {self.flight}"
    
    
    


#--------------------------------------------------------------#

class BookingAccommodation(models.Model):

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name='accommodations'
    )

    accommodation = models.ForeignKey(
        'tours.Accommodation',
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

    price = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        default=0
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.booking} - {self.accommodation}"
    
    
    
    
#----------------------------------------------------------#

class Refund(models.Model):

    booking_item = models.ForeignKey(
        BookingItem,
        on_delete=models.CASCADE,
        related_name='refunds'
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=0
    )

    reason = models.CharField(
        max_length=255
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.booking_item} - "
            f"{self.amount}"
        )