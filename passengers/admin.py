from django.contrib import admin
from .models import Passenger, Passport, Document


class PassportInline(admin.StackedInline):
    model = Passport
    extra = 0
    
    
class DocumentInline(admin.TabularInline):
    model = Document
    extra = 0
    
    
class DocumentInline(admin.TabularInline):
    model = Document
    extra = 0
    
@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):

    list_display = (
        'customer_code',
        'first_name',
        'last_name',
        'phone',
        'national_code',
        'created_at'
    )

    search_fields = (
        'customer_code',
        'first_name',
        'last_name',
        'phone',
        'national_code'
    )
    
    readonly_fields = (
    'customer_code',
    )

    ordering = (
        '-created_at',
    )

    list_per_page = 25

    inlines = [
        PassportInline,
        DocumentInline
    ]
    
@admin.register(Passport)
class PassportAdmin(admin.ModelAdmin):

    list_display = (
        'passport_number',
        'passenger',
        'expiry_date'
    )

    search_fields = (
        'passport_number',
        'passenger__first_name',
        'passenger__last_name'
    )
    
    
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'passenger',
        'document_type',
        'uploaded_at'
    )

    list_filter = (
        'document_type',
        'uploaded_at'
    )

    search_fields = (
        'title',
        'passenger__first_name',
        'passenger__last_name',
        'passenger__customer_code'
    )