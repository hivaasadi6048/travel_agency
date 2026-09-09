from django.contrib import admin
from .models import Tour, Country, City,Accommodation,TourAccommodation,Flight,TourFlight,Visa



class TourAccommodationInline(admin.TabularInline):
    model = TourAccommodation
    extra = 1
    
    
class TourFlightInline(admin.TabularInline):
    model = TourFlight
    extra = 1

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):

    list_display = (
        'tour_code',
        'title',
        'destination',
        'departure_date',
        'capacity',
        'status',
    )

    search_fields = (
        'tour_code',
        'title',
        'destination',
    )

    list_filter = (
        'status',
        'destination',
    )

    readonly_fields = (
        'tour_code',
    )

    ordering = (
        '-departure_date',
    )
    
    inlines = (
    TourAccommodationInline,
    )
    
    
    inlines = (TourAccommodationInline,TourFlightInline,)
    
    
@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):

    search_fields = (
        'name',
        'code',
    )

    list_display = (
        'name',
        'code',
    )
    
    
@admin.register(City)
class CityAdmin(admin.ModelAdmin):

    search_fields = (
        'name',
    )

    list_display = (
        'name',
        'country',
    )

    list_filter = (
        'country',
    )
    

@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'type',
        'city',
    )

    list_filter = (
        'type',
        'city',
    )

    search_fields = (
        'name',
        'phone',
    )
    
    
@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):

    list_display = (
        'from_city',
        'to_city',
        'transport_type',
        'flight_number',
    )

    list_filter = (
        'transport_type',
        'from_city',
        'to_city',
    )

    search_fields = (
        'flight_number',
        'airline',
    )
    
    
@admin.register(Visa)
class VisaAdmin(admin.ModelAdmin):

    list_display = (
        'country',
        'visa_type',
        'price',
        'processing_days',
    )

    search_fields = (
        'visa_type',
        'country__name',
    )

    list_filter = (
        'country',
    )
    

