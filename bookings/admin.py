from django.contrib import admin
from .models import Booking, BookingItem
from payments.models import Payment
from .models import *





class BookingItemInline(admin.TabularInline):
    model = BookingItem
    extra = 1
    
    
class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    
    
    
class BookingVisaInline(admin.TabularInline):
    model = BookingVisa
    extra = 1
    autocomplete_fields = ('visa',)
    show_change_link = True
    
    
    
class BookingFlightInline(admin.TabularInline):
    model = BookingFlight
    extra = 1
    autocomplete_fields = ('flight',)
    show_change_link = True
    
    
    
class BookingAccommodationInline(admin.TabularInline):
    model = BookingAccommodation
    extra = 1
    autocomplete_fields = ('accommodation',)
    show_change_link = True
    
    
    
    


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        'booking_code',
        'passenger',
        'status',
        'total_price',
        'paid_amount',
        'remaining_amount',
        'created_at'
    )

    list_filter = (
        'status',
        'created_at'
    )

    search_fields = (
        'booking_code',
        'passenger__first_name',
        'passenger__last_name',
        'passenger__customer_code'
    )

    readonly_fields = (
        'booking_code',
        'created_at',
        'updated_at'
    )

    ordering = (
        '-created_at',
    )
    
    
    inlines = [
    BookingItemInline,
    PaymentInline,
    BookingVisaInline,
    BookingFlightInline,
    BookingAccommodationInline
    ]


@admin.register(BookingItem)
class BookingItemAdmin(admin.ModelAdmin):

    list_display = (
        'booking',
        'item_type',
        'price'
    )

    list_filter = (
        'item_type',
    )

    search_fields = (
        'booking__booking_code',
    )


@admin.register(BookingVisa)
class BookingVisaAdmin(admin.ModelAdmin):

    list_display = (
        'booking',
        'visa',
        'quantity',
        'price',
        'created_at'
    )

    list_filter = (
        'visa__country',
        'created_at'
    )

    search_fields = (
        'booking__booking_code',
        'visa__visa_type',
        'visa__country__name'
    )

    ordering = (
        '-created_at',
    )


@admin.register(BookingFlight)
class BookingFlightAdmin(admin.ModelAdmin):

    list_display = (
        'booking',
        'flight',
        'quantity',
        'price',
        'created_at'
    )

    list_filter = (
        'created_at',
    )

    search_fields = (
        'booking__booking_code',
        'flight__airline',
        'flight__flight_number'
    )

    ordering = (
        '-created_at',
    )


@admin.register(BookingAccommodation)
class BookingAccommodationAdmin(admin.ModelAdmin):

    list_display = (
        'booking',
        'accommodation',
        'check_in_date',
        'check_out_date',
        'nights',
        'price'
    )

    list_filter = (
        'check_in_date',
        'check_out_date'
    )

    search_fields = (
        'booking__booking_code',
        'accommodation__name'
    )

    ordering = (
        '-id',
    )
    
    
    
@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):

    list_display = (
        'booking_item',
        'amount',
        'reason',
        'created_at'
    )

    list_filter = (
        'created_at',
    )

    search_fields = (
        'booking_item__booking__booking_code',
        'reason',
    )

    readonly_fields = (
        'created_at',
    )

    ordering = (
        '-created_at',
    )