from django.db import models


class Payment(models.Model):

    PAYMENT_METHODS = (
        ('cash', 'نقدی'),
        ('card', 'کارت به کارت'),
        ('online', 'پرداخت آنلاین'),
        ('installment', 'اقساطی'),
    )

    booking = models.ForeignKey(
        'bookings.Booking',
        on_delete=models.CASCADE,
        related_name='payments'
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=0
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS
    )

    paid_at = models.DateTimeField(
        auto_now_add=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.booking.booking_code} - {self.amount}"
    
    
    
    
    
    
class Expense(models.Model):

    CATEGORY_CHOICES = (

        ('hotel', 'هتل'),
        ('airline', 'ایرلاین'),
        ('driver', 'راننده'),
        ('guide', 'راهنما'),
        ('train', 'قطار'),
        ('bus', 'اتوبوس'),
        ('insurance', 'بیمه'),
        ('advertising', 'تبلیغات'),
        ('office', 'هزینه دفتر'),
        ('other', 'سایر'),

    )
    
    booking = models.ForeignKey(
    'bookings.Booking',
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='expenses'
    )
    

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES
    )

    title = models.CharField(
        max_length=200
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=0
    )

    paid_at = models.DateField()
    

    description = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
    
    

    def __str__(self):

        return (
            f"{self.get_category_display()} - "
            f"{self.title}"
        )