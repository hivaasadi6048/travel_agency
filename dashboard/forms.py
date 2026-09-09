from django import forms
from passengers.models import Passenger,Document,Passport
from bookings.models import Booking
from bookings.models import BookingItem
from tours.models import Tour
from tours.models import Flight
from tours.models import Visa
from tours.models import Accommodation
from bookings.models import Refund
from payments.models import Expense

class PassengerForm(forms.ModelForm):

    class Meta:

        model = Passenger

        fields = [

            'first_name',
            'last_name',
            'national_code',
            'birth_date',
            'phone',
            'email',
            'address',
            'notes',

        ]

        labels = {

            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'national_code': 'کد ملی',
            'birth_date': 'تاریخ تولد',
            'phone': 'تلفن',
            'email': 'ایمیل',
            'address': 'آدرس',
            'notes': 'توضیحات',

        }
        
        



class BookingForm(forms.ModelForm):

    class Meta:

        model = Booking

        fields = [

            'passenger',
            'status',
            'total_price',

        ]

        labels = {

            'passenger': 'مسافر',
            'status': 'وضعیت',
            'total_price': 'مبلغ کل',

        }
        
        



class BookingTourForm(forms.ModelForm):

    class Meta:

        model = BookingItem

        fields = [

            'tour',
            'price',
            'notes'

        ]

        labels = {

            'tour': 'تور',
            'price': 'قیمت توافقی',
            'notes': 'توضیحات'

        }
        
        



class BookingFlightForm(forms.ModelForm):

    class Meta:

        model = BookingItem

        fields = [

            'flight',
            'price',
            'notes'

        ]

        labels = {

            'flight': 'پرواز',
            'price': 'قیمت توافقی',
            'notes': 'توضیحات'

        }
        
        
        



class BookingVisaForm(forms.ModelForm):

    class Meta:

        model = BookingItem

        fields = [

            'visa',
            'price',
            'notes'

        ]

        labels = {

            'visa': 'ویزا',
            'price': 'قیمت توافقی',
            'notes': 'توضیحات'

        }
        
        
        



class BookingAccommodationForm(forms.ModelForm):

    class Meta:

        model = BookingItem

        fields = [
            'accommodation',
            'price',
            'notes'
        ]

        labels = {
            'accommodation': 'اقامتگاه',
            'price': 'قیمت توافقی',
            'notes': 'توضیحات'
        }
        
        

class BookingItemEditForm(forms.ModelForm):

    class Meta:

        model = BookingItem

        fields = [

            'item_type',

            'tour',

            'flight',

            'accommodation',

            'visa',

            'price',

            'notes',

        ]

        labels = {

            'item_type': 'نوع خدمت',

            'tour': 'تور',

            'flight': 'پرواز',

            'accommodation': 'اقامتگاه',

            'visa': 'ویزا',

            'price': 'قیمت توافقی',

            'notes': 'توضیحات',

        }


class AccommodationForm(forms.ModelForm):

    class Meta:

        model = Accommodation

        fields = [
            'name',
            'type',
            'city',
            'address',
            'phone',
            'description'
        ]

        labels = {
            'name': 'نام اقامتگاه',
            'type': 'نوع اقامتگاه',
            'city': 'شهر',
            'address': 'آدرس',
            'phone': 'تلفن',
            'description': 'توضیحات'
        }
        
        
from tours.models import Visa


class VisaForm(forms.ModelForm):

    class Meta:

        model = Visa

        fields = [
            'country',
            'visa_type',
            'processing_days',
            'validity_days',
            'price',
            'notes'
        ]

        labels = {
            'country': 'کشور',
            'visa_type': 'نوع ویزا',
            'processing_days': 'مدت زمان صدور',
            'validity_days': 'مدت اعتبار',
            'price': 'قیمت',
            'notes': 'توضیحات'
        }
        
        
from tours.models import Flight


class FlightForm(forms.ModelForm):

    class Meta:

        model = Flight

        fields = [
            'transport_type',
            'from_city',
            'to_city',
            'airline',
            'flight_number',
            'departure_time',
            'arrival_time',
            'price',
            'notes'
        ]

        labels = {
            'transport_type': 'نوع وسیله',
            'from_city': 'مبدا',
            'to_city': 'مقصد',
            'airline': 'شرکت',
            'flight_number': 'شماره',
            'departure_time': 'زمان حرکت',
            'arrival_time': 'زمان رسیدن',
            'price': 'قیمت',
            'notes': 'توضیحات'
        }
        
        
from tours.models import Tour


class TourForm(forms.ModelForm):

    class Meta:

        model = Tour

        fields = [
            'title',
            'destination',
            'destination_city',
            'departure_date',
            'return_date',
            'capacity',
            'adult_price',
            'child_price',
            'services',
            'description',
            'status'
        ]

        labels = {
            'title': 'عنوان تور',
            'destination': 'مقصد',
            'destination_city': 'شهر مقصد',
            'departure_date': 'تاریخ حرکت',
            'return_date': 'تاریخ برگشت',
            'capacity': 'ظرفیت',
            'adult_price': 'قیمت بزرگسال',
            'child_price': 'قیمت کودک',
            'services': 'خدمات',
            'description': 'توضیحات',
            'status': 'وضعیت'
        }
        
        
        
from tours.models import TourFlight


class TourFlightForm(forms.ModelForm):

    class Meta:

        model = TourFlight

        fields = [
            'flight',
            'order',
            'date',
            'notes'
        ]

        labels = {
            'flight': 'پرواز',
            'order': 'ترتیب',
            'date': 'تاریخ',
            'notes': 'توضیحات'
        }
        
        
        
#افزودن اقامتگاه به تور#
from tours.models import TourAccommodation


class TourAccommodationForm(forms.ModelForm):

    class Meta:

        model = TourAccommodation

        fields = [
            'accommodation',
            'check_in_date',
            'check_out_date',
            'nights',
            'order',
            'notes'
        ]

        labels = {
            'accommodation': 'اقامتگاه',
            'check_in_date': 'تاریخ ورود',
            'check_out_date': 'تاریخ خروج',
            'nights': 'تعداد شب',
            'order': 'ترتیب',
            'notes': 'توضیحات'
        }
        
        
from tours.models import Country


class CountryForm(forms.ModelForm):

    class Meta:

        model = Country

        fields = [
            'name',
            'code'
        ]

        labels = {
            'name': 'نام کشور',
            'code': 'کد کشور'
        }
        
        
from tours.models import City


class CityForm(forms.ModelForm):

    class Meta:

        model = City

        fields = [
            'country',
            'name'
        ]

        labels = {
            'country': 'کشور',
            'name': 'نام شهر'
        }
        
        
        


class RefundForm(forms.ModelForm):

    class Meta:

        model = Refund

        fields = [
            'amount',
            'reason',
            'notes'
        ]
        
        labels = {
            'amount':'مبلغ',
            'reason':'دلیل',
            'notes':'توضیحات'
        }
        
        
        
        
class ExpenseForm(forms.ModelForm):

    class Meta:

        model = Expense

        fields = [
            
            'category',
            'title',
            'amount',
            'paid_at',
            'description',
        ]
        
        
        
        
#فرم مدارک#
class DocumentForm(forms.ModelForm):

    class Meta:

        model = Document

        fields = [
            'title',
            'document_type',
            'file',
            'expiry_date',
            'notes',
        ]        
        
        
#فرم ثبت پایپورت#    
class PassportForm(forms.ModelForm):

    class Meta:

        model = Passport

        fields = [
            'passport_number',
            'issue_date',
            'expiry_date',
            'country',
            
        ]