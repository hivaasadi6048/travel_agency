from django.contrib import admin
from .models import Payment,Expense



@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        'booking',
        'amount',
        'payment_method',
        'paid_at',
    )

    list_filter = (
        'payment_method',
        'paid_at',
    )

    search_fields = (
        'booking__booking_code',
    )
    
    
    
@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'booking',
        'category',
        'amount',
        'paid_at',
        'created_at',
    )

    list_filter = (
        'category',
        'paid_at',
        'booking',
    )

    search_fields = (
        'title',
        'description',
        'booking__booking_code',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    ordering = (
        '-paid_at',
    )

    fieldsets = (

        (
            'اطلاعات هزینه',
            {
                'fields': (
                    'booking',
                    'category',
                    'title',
                    'amount',
                    'paid_at',
                )
            }
        ),

        (
            'توضیحات',
            {
                'fields': (
                    'description',
                )
            }
        ),

        (
            'اطلاعات سیستم',
            {
                'fields': (
                    'created_at',
                    'updated_at',
                )
            }
        ),

    )    