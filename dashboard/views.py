from decimal import Decimal
from datetime import date, timedelta
from openpyxl import Workbook
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import (Sum, F, ExpressionWrapper, DecimalField, Value,Q)
from django.db.models.functions import Coalesce
from django.shortcuts import (render, redirect, get_object_or_404)
from passengers.models import Passenger,Passport,Document
from bookings.models import (Booking,BookingItem,Refund,)
from payments.models import (Payment,Expense,)
from tours.models import (Tour,Visa,Flight,Country,City,TourFlight,TourAccommodation,Accommodation,)
from .forms import (
    PassengerForm,
    BookingForm,
    BookingTourForm,
    BookingFlightForm,
    BookingVisaForm,
    BookingAccommodationForm,
    BookingItemEditForm,
    AccommodationForm,
    VisaForm,
    FlightForm,
    TourForm,
    TourFlightForm,
    TourAccommodationForm,
    CountryForm,
    CityForm,
    RefundForm,
    ExpenseForm,
    DocumentForm,
    PassportForm
)

#----------------------------------------------صفحه داشبورد #
@login_required
def dashboard_view(request):

    total_sales = 0

    for booking in Booking.objects.prefetch_related('items'):
        total_sales += booking.actual_total_price

    total_payments = Payment.objects.aggregate(
        total=Sum('amount')
    )['total'] or 0

    total_refunds = Refund.objects.aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    total_expenses = Expense.objects.aggregate(
        total=Sum('amount')
    )['total'] or 0

    net_profit = (
        total_sales
        - total_expenses
    )

    total_debts = max(
        0,
        total_sales - total_payments
    )
    
    
    debtors = []

    for booking in Booking.objects.select_related(
        'passenger'
    ):

        if booking.remaining_amount > 0:

            debtors.append(booking)
    
    expired_passports = Passport.objects.filter(
        expiry_date__lte=date.today()
    )

    expiring_passports = Passport.objects.filter(
        expiry_date__gt=date.today(),
        expiry_date__lte=date.today() + timedelta(days=180)
        )
    
    
    tour_sales = BookingItem.objects.filter(
        item_type='tour'
    ).count()

    flight_sales = BookingItem.objects.filter(
        item_type='flight'
    ).count()

    accommodation_sales = BookingItem.objects.filter(
        item_type='accommodation'
    ).count()

    visa_sales = BookingItem.objects.filter(
        item_type='visa'
    ).count()


    tour_amount = 0
    flight_amount = 0
    accommodation_amount = 0
    visa_amount = 0

    for item in BookingItem.objects.all():

        if item.item_type == 'tour':
            tour_amount += item.final_price

        elif item.item_type == 'flight':
            flight_amount += item.final_price

        elif item.item_type == 'accommodation':
            accommodation_amount += item.final_price

        elif item.item_type == 'visa':
            visa_amount += item.final_price

    context = {

        'passenger_count': Passenger.objects.count(),

        'booking_count': Booking.objects.count(),

        'total_sales': total_sales,

        'total_payments': total_payments,

        'total_refunds': total_refunds,

        'total_debts': total_debts,
        
        'expired_passports': expired_passports,
        
        'expiring_passports': expiring_passports,
        
        'total_expenses': total_expenses,

        'net_profit': net_profit,

        'debtors': debtors,

        'tour_sales': tour_sales,

        'flight_sales': flight_sales,

        'accommodation_sales': accommodation_sales,

        'visa_sales': visa_sales,
        
        'tour_amount': tour_amount,

        'flight_amount': flight_amount,

        'accommodation_amount': accommodation_amount,

        'visa_amount': visa_amount,

    }

    return render(
        request,
        'dashboard/dashboard.html',
        context
    )

   
#------------------------------------------------سرچ سراسری#

@login_required
def global_search(request):

    query = request.GET.get('q', '').strip()

    passengers = Passenger.objects.none()
    bookings = Booking.objects.none()

    if query:

        passengers = Passenger.objects.filter(

            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(customer_code__icontains=query) |
            Q(phone__icontains=query) |
            Q(email__icontains=query) |
            Q(passport__passport_number__icontains=query)

        ).distinct()

        bookings = Booking.objects.select_related(
            'passenger'
        ).filter(

            Q(booking_code__icontains=query) |
            Q(passenger__first_name__icontains=query) |
            Q(passenger__last_name__icontains=query) |
            Q(passenger__customer_code__icontains=query)

        ).distinct()

    context = {

        'query': query,
        'passengers': passengers,
        'bookings': bookings,

    }

    return render(
        request,
        'dashboard/search_results.html',
        context
    )
#---------------------------------------بخش مسافران #

@login_required
def passenger_list(request):

    query = request.GET.get('q')

    passengers = Passenger.objects.all()

    if query:
        passengers = passengers.filter(
            first_name__icontains=query
        ) | passengers.filter(
            last_name__icontains=query
        ) | passengers.filter(
            customer_code__icontains=query
        )

    context = {
        'passengers': passengers,
        'query': query
    }

    return render(
        request,
        'dashboard/passengers/list.html',
        context
    )
    
    
    
    
#---------------------------------------------جزئیات مسافر#
    
@login_required
def passenger_detail(request, pk):

    passenger = get_object_or_404(
        Passenger.objects.prefetch_related(
            'documents'
        ),
        pk=pk
    )

    bookings = Booking.objects.filter(
        passenger=passenger
    )

    total_debt = 0

    for booking in bookings:

        total_debt += booking.remaining_amount

    payments = Payment.objects.filter(
        booking__passenger=passenger
    ).order_by(
        '-paid_at'
    )

    passport = getattr(
        passenger,
        'passport',
        None
    )
    
    passport_documents = passenger.documents.filter(
    document_type='passport_image'
    )

    other_documents = passenger.documents.exclude(
    document_type='passport_image'
    )

    context = {

        'passenger': passenger,

        'passport': getattr(passenger, 'passport', None),

        'bookings': bookings,

        'payments': payments,

        'total_debt': total_debt,
        
        'passport_documents': passport_documents,
        
        'other_documents': other_documents,

    }

    return render(
        request,
        'dashboard/passengers/detail.html',
        context
    )
#---------------------------------------اضافه کردن مسافر جدید#    
@login_required
def passenger_create(request):

    if request.method == 'POST':

        form = PassengerForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect(
                'dashboard:passengers'
            )

    else:

        form = PassengerForm()

    context = {

        'form': form

    }

    return render(
        request,
        'dashboard/passengers/create.html',
        context
    )
    
    
#--------------------------------------ویرایش مسافر جدید#
@login_required
def passenger_edit(request, pk):

    passenger = get_object_or_404(
        Passenger,
        pk=pk
    )

    if request.method == 'POST':

        form = PassengerForm(
            request.POST,
            instance=passenger
        )

        if form.is_valid():

            form.save()

            return redirect(
                'dashboard:passenger_detail',
                pk=passenger.id
            )

    else:

        form = PassengerForm(
            instance=passenger
        )

    context = {

        'form': form,
        'passenger': passenger

    }

    return render(
        request,
        'dashboard/passengers/edit.html',
        context
    )
    
    
#-----------------------------------------------حذف مسافر#

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

@login_required
def delete_passenger(request, pk):

    passenger = get_object_or_404(
        Passenger,
        pk=pk
    )

    if request.method == 'POST':

        passenger.delete()

        messages.success(
            request,
            'مسافر با موفقیت حذف شد.'
        )

        return redirect(
            'dashboard:passengers'
        )

    return render(
        request,
        'dashboard/passengers/delete.html',
        {
            'passenger': passenger
        }
    )

#-----------------------------------------------پرداخت ها#

@login_required
def payment_list(request):

    payments = Payment.objects.all().order_by(
        '-paid_at'
    )

    return render(
        request,
        'dashboard/payments/list.html',
        {
            'payments': payments
        }
    )
    
    
    

#----------------------------------------اضافه کردن پرداختی#

@login_required
def add_payment(request, pk):

    passenger = get_object_or_404(
        Passenger,
        pk=pk
    )

    if request.method == 'POST':

        booking_id = request.POST.get(
            'booking_id'
        )

        amount = request.POST.get(
            'amount'
        )

        payment_method = request.POST.get(
            'payment_method'
        )

        booking = get_object_or_404(
            Booking,
            id=booking_id,
            passenger=passenger
        )

        amount = Decimal(amount)
        
        if amount <= 0:
            bookings = Booking.objects.filter(
                passenger=passenger
            )

            return render(
                request,
                'dashboard/passengers/add_payment.html',
                {
                    'passenger': passenger,
                    'bookings': bookings,
                    'error': 'مبلغ باید بزرگتر از صفر باشد.'
                }
            )

        if amount > booking.remaining_amount:

            bookings = Booking.objects.filter(
                passenger=passenger
            )

            return render(
                request,
                'dashboard/passengers/add_payment.html',
                {
                    'passenger': passenger,
                    'bookings': bookings,
                    'error': 'مبلغ پرداخت بیشتر از بدهی باقی‌مانده است.'
                }
            )

        Payment.objects.create(
            booking=booking,
            amount=amount,
            payment_method=payment_method
        )

        return redirect(
            'dashboard:passenger_detail',
            pk=passenger.id
        )

    bookings = Booking.objects.filter(
        passenger=passenger
    )

    return render(
        request,
        'dashboard/passengers/add_payment.html',
        {
            'passenger': passenger,
            'bookings': bookings
        }
    )



#-----------------------------------بخش ورود و خروج کاربر#
    
def login_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')

    if request.method == 'POST':

        username = request.POST.get('username')

        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            login(request, user)

            return redirect(
                'dashboard:dashboard'
            )

    return render(
        request,
        'dashboard/login.html'
    )
    



    
def logout_view(request):

    logout(request)

    return redirect(
        'dashboard:login'
    )
    
    
    
    
    
    


#--------------------------------------------لیست رزروها#
def bookings_list(request):

    query = request.GET.get('q')

    bookings = Booking.objects.select_related(
        'passenger'
    ).order_by('-id')

    if query:

        bookings = bookings.filter(
            booking_code__icontains=query
        ) | bookings.filter(
            passenger__first_name__icontains=query
        ) | bookings.filter(
            passenger__last_name__icontains=query
        )

    context = {

        'bookings': bookings,
        'query': query

    }

    return render(
        request,
        'dashboard/bookings/list.html',
        context
    )

#------------------------------------------ساخت رزروها#  
@login_required
def booking_create(request):

    if request.method == 'POST':

        form = BookingForm(request.POST)

        if form.is_valid():

            booking = form.save()

            return redirect(
                'dashboard:bookings'
            )

    else:

        form = BookingForm()

    context = {

        'form': form

    }

    return render(
        request,
        'dashboard/bookings/create.html',
        context
    )
    



#--------------------------------------حذف رزرو#

@login_required
def delete_booking(request, pk):

    booking = get_object_or_404(
        Booking,
        pk=pk
    )

    if request.method == 'POST':

        booking.delete()

        return redirect(
            'dashboard:bookings'
        )

    return render(
        request,
        'dashboard/bookings/delete.html',
        {
            'booking': booking
        }
    )
    
    

#--------------------------------------جزئیات رزرو#
@login_required
def booking_detail(request, pk):

    booking = get_object_or_404(
        Booking.objects.select_related(
            'passenger'
        ).prefetch_related(
            'items',
            'items__refunds',
            'expenses',
        ),
        pk=pk
    )

    booking_expenses = Expense.objects.filter(
        booking=booking
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    booking_profit = (
        booking.actual_total_price
        - booking_expenses
    )

    context = {

        'booking': booking,

        'booking_expenses': booking_expenses,

        'booking_profit': booking_profit,

    }

    return render(
        request,
        'dashboard/bookings/detail.html',
        context
    )
    
#------------------------------------اضافه کردن تورها به رزروها#       
@login_required
def add_tour_to_booking(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id
    )

    if request.method == 'POST':

        form = BookingTourForm(
            request.POST
        )

        if form.is_valid():

            item = form.save(
                commit=False
            )

            item.booking = booking

            item.item_type = 'tour'

            item.save()

            return redirect(
                'dashboard:booking_detail',
                pk=booking.id
            )

    else:

        form = BookingTourForm()

    context = {

        'booking': booking,
        'form': form

    }

    return render(
        request,
        'dashboard/bookings/add_tour.html',
        context
    )
    
#-----------------------------------اضافه کردن پروازها به رزروها#       
@login_required
def add_flight_to_booking(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id
    )

    if request.method == 'POST':

        form = BookingFlightForm(
            request.POST
        )

        if form.is_valid():

            item = form.save(
                commit=False
            )

            item.booking = booking

            item.item_type = 'flight'

            item.save()

            return redirect(
                'dashboard:booking_detail',
                pk=booking.id
            )

    else:

        form = BookingFlightForm()

    return render(
        request,
        'dashboard/bookings/add_flight.html',
        {
            'booking': booking,
            'form': form
        }
    )    
    
    
#------------------------------------اضافه کردن ویزا به رزروها#      
@login_required
def add_visa_to_booking(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id
    )

    if request.method == 'POST':

        form = BookingVisaForm(
            request.POST
        )

        if form.is_valid():

            item = form.save(
                commit=False
            )

            item.booking = booking

            item.item_type = 'visa'

            item.save()

            return redirect(
                'dashboard:booking_detail',
                pk=booking.id
            )

    else:

        form = BookingVisaForm()

    return render(
        request,
        'dashboard/bookings/add_visa.html',
        {
            'booking': booking,
            'form': form
        }
    )
    
    
#--------------------------------اضافه کردن اقامتگاه به رزروها#   
@login_required
def add_accommodation_to_booking(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id
    )

    if request.method == 'POST':

        form = BookingAccommodationForm(
            request.POST
        )

        if form.is_valid():

            item = form.save(
                commit=False
            )

            item.booking = booking

            item.item_type = 'accommodation'

            item.save()

            return redirect(
                'dashboard:booking_detail',
                pk=booking.id
            )

    else:

        form = BookingAccommodationForm()

    return render(
        request,
        'dashboard/bookings/add_accommodation.html',
        {
            'booking': booking,
            'form': form
        }
    )    
    
    
 #---------------------------------------------حذف  رزروها#   
@login_required
def delete_booking_item(request, pk):

    item = get_object_or_404(
        BookingItem,
        pk=pk
    )

    booking_id = item.booking.id

    item.delete()

    return redirect(
        'dashboard:booking_detail',
        pk=booking_id
    )
    
    
    
#----------------------------------------------------ویرایش رزرو#

@login_required
def edit_booking(request, pk):

    booking = get_object_or_404(
        Booking,
        pk=pk
    )

    if request.method == 'POST':

        form = BookingForm(
            request.POST,
            instance=booking
        )

        if form.is_valid():

            form.save()

            return redirect(
                'dashboard:booking_detail',
                pk=booking.id
            )

    else:

        form = BookingForm(
            instance=booking
        )

    context = {

        'form': form,

        'booking': booking,

        'items': booking.items.all(),

    }

    return render(
        request,
        'dashboard/bookings/edit_booking.html',
        context
    )
    
#----------------------------------------ویرایش  آیتم رزروها#     
@login_required
def edit_booking_item(request, pk):

    item = get_object_or_404(
        BookingItem,
        pk=pk
    )

    if request.method == 'POST':

        form = BookingItemEditForm(
            request.POST,
            instance=item
        )

        if form.is_valid():

            item = form.save(commit=False)

            if item.item_type == 'tour':

                item.flight = None
                item.accommodation = None
                item.visa = None

            elif item.item_type == 'flight':

                item.tour = None
                item.accommodation = None
                item.visa = None

            elif item.item_type == 'accommodation':

                item.tour = None
                item.flight = None
                item.visa = None

            elif item.item_type == 'visa':

                item.tour = None
                item.flight = None
                item.accommodation = None

            item.save()

            return redirect(
                'dashboard:booking_detail',
                pk=item.booking.id
            )

    else:

        form = BookingItemEditForm(
            instance=item
        )

    return render(
        request,
        'dashboard/bookings/edit_item.html',
        {
            'form': form,
            'item': item
        }
    )
#---------------------------------------مدیریت اقامتگاه#



@login_required
def accommodation_list(request):

    accommodations = Accommodation.objects.all().order_by('name')

    return render(
        request,
        'dashboard/accommodations/list.html',
        {
            'accommodations': accommodations
        }
    )
    
    
#------------------------------------اضافه کردن اقامتگاه#
@login_required
def add_accommodation(request):

    if request.method == 'POST':

        form = AccommodationForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            return redirect(
                'dashboard:accommodation_list'
            )

    else:

        form = AccommodationForm()

    return render(
        request,
        'dashboard/accommodations/add.html',
        {
            'form': form
        }
    )
    
    
#-----------------------------------------ویرایش اقامتگاه#
@login_required
def edit_accommodation(request, pk):

    accommodation = get_object_or_404(
        Accommodation,
        pk=pk
    )

    if request.method == 'POST':

        form = AccommodationForm(
            request.POST,
            instance=accommodation
        )

        if form.is_valid():

            form.save()

            return redirect(
                'dashboard:accommodation_list'
            )

    else:

        form = AccommodationForm(
            instance=accommodation
        )

    return render(
        request,
        'dashboard/accommodations/edit.html',
        {
            'form': form,
            'accommodation': accommodation
        }
    )
    
    
#-------------------------------------------حذف اقامتگاه#
@login_required
def delete_accommodation(request, pk):

    accommodation = get_object_or_404(
        Accommodation,
        pk=pk
    )

    try:

        accommodation.delete()

        messages.success(
            request,
            'اقامتگاه با موفقیت حذف شد.'
        )

    except Exception:

        messages.error(
            request,
            'این اقامتگاه در رزرو یا تور استفاده شده و قابل حذف نیست.'
        )

    return redirect(
        'dashboard:accommodation_list'
    )
    
    
    
#--------------------------------------------لیست ویزاها#
@login_required
def visa_list(request):

    visas = Visa.objects.all().order_by(
        'country'
    )

    return render(
        request,
        'dashboard/visas/list.html',
        {
            'visas': visas
        }
    )
    
    
#-------------------------------------------افزودن ویزا#
@login_required
def add_visa(request):

    if request.method == 'POST':

        form = VisaForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect(
                'dashboard:visa_list'
            )

    else:

        form = VisaForm()

    return render(
        request,
        'dashboard/visas/add.html',
        {
            'form': form
        }
    )
    
    
#-----------------------------------------ویرایش ویزا#
@login_required
def edit_visa(request, pk):

    visa = get_object_or_404(
        Visa,
        pk=pk
    )

    if request.method == 'POST':

        form = VisaForm(
            request.POST,
            instance=visa
        )

        if form.is_valid():

            form.save()

            return redirect(
                'dashboard:visa_list'
            )

    else:

        form = VisaForm(
            instance=visa
        )

    return render(
        request,
        'dashboard/visas/edit.html',
        {
            'form': form,
            'visa': visa
        }
    )
    
    
#---------------------------------حذف ویزا#
@login_required
def delete_visa(request, pk):

    visa = get_object_or_404(
        Visa,
        pk=pk
    )

    try:

        visa.delete()

        messages.success(
            request,
            'ویزا با موفقیت حذف شد'
        )

    except Exception:

        messages.error(
            request,
            'این ویزا در رزروها استفاده شده و قابل حذف نیست'
        )

    return redirect(
        'dashboard:visa_list'
    )
    
    
    
    
#-----------------------------------------------لیست پروازها#
@login_required
def flight_list(request):

    flights = Flight.objects.all().order_by('-id')

    return render(
        request,
        'dashboard/flights/list.html',
        {
            'flights': flights
        }
    )
    
    
#------------------------------------------افزودن پروازها#
@login_required
def add_flight(request):

    if request.method == 'POST':

        form = FlightForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect(
                'dashboard:flight_list'
            )

    else:

        form = FlightForm()

    return render(
        request,
        'dashboard/flights/add.html',
        {
            'form': form
        }
    )
    
    
#-----------------------------------------ویرایش پروازها#
@login_required
def edit_flight(request, pk):

    flight = get_object_or_404(
        Flight,
        pk=pk
    )

    if request.method == 'POST':

        form = FlightForm(
            request.POST,
            instance=flight
        )

        if form.is_valid():

            form.save()

            return redirect(
                'dashboard:flight_list'
            )

    else:

        form = FlightForm(
            instance=flight
        )

    return render(
        request,
        'dashboard/flights/edit.html',
        {
            'form': form,
            'flight': flight
        }
    )
    
    
#--------------------------------------------حذف پروازها#
@login_required
def delete_flight(request, pk):

    flight = get_object_or_404(
        Flight,
        pk=pk
    )

    try:

        flight.delete()

        messages.success(
            request,
            'پرواز حذف شد'
        )

    except Exception:

        messages.error(
            request,
            'این پرواز در رزروها استفاده شده است'
        )

    return redirect(
        'dashboard:flight_list'
    )
    
    
#------------------------------------------لیست تورها#
@login_required
def tour_list(request):

    tours = Tour.objects.all().order_by(
        '-departure_date'
    )

    return render(
        request,
        'dashboard/tours/list.html',
        {
            'tours': tours
        }
    )
    
    
#-------------------------------------------افزودن تور#
@login_required
def add_tour(request):

    if request.method == 'POST':

        form = TourForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect(
                'dashboard:tour_list'
            )

    else:

        form = TourForm()

    return render(
        request,
        'dashboard/tours/add.html',
        {
            'form': form
        }
    )
    
    
    
#-----------------------------------------------ویرایش تور#
@login_required
def edit_tour(request, pk):

    tour = get_object_or_404(
        Tour,
        pk=pk
    )

    if request.method == 'POST':

        form = TourForm(
            request.POST,
            instance=tour
        )

        if form.is_valid():

            form.save()

            return redirect(
                'dashboard:tour_list'
            )

    else:

        form = TourForm(
            instance=tour
        )

    return render(
        request,
        'dashboard/tours/edit.html',
        {
            'form': form,
            'tour': tour
        }
    )
    
    
#----------------------------------------------حذف تور#
@login_required
def delete_tour(request, pk):

    tour = get_object_or_404(
        Tour,
        pk=pk
    )

    try:

        tour.delete()

        messages.success(
            request,
            'تور حذف شد'
        )

    except Exception:

        messages.error(
            request,
            'این تور در رزروها استفاده شده است'
        )

    return redirect(
        'dashboard:tour_list'
    )
    
    
    
#-------------------------------------------جزئیات تور#
@login_required
def tour_detail(request, pk):

    tour = get_object_or_404(
        Tour,
        pk=pk
    )

    flights = tour.flights.all()

    accommodations = tour.accommodations.all()

    return render(
        request,
        'dashboard/tours/detail.html',
        {
            'tour': tour,
            'flights': flights,
            'accommodations': accommodations
        }
    )
    
    
    
#--------------------------------------افزودن پرواز به تور#
@login_required
def add_tour_flight(request, tour_id):

    tour = get_object_or_404(
        Tour,
        id=tour_id
    )

    if request.method == 'POST':

        form = TourFlightForm(
            request.POST
        )

        if form.is_valid():

            tour_flight = form.save(
                commit=False
            )

            tour_flight.tour = tour

            tour_flight.save()

            return redirect(
                'dashboard:tour_detail',
                pk=tour.id
            )

    else:

        form = TourFlightForm()

    return render(
        request,
        'dashboard/tours/add_flight.html',
        {
            'tour': tour,
            'form': form
        }
    )
    
    
#------------------------------------افزودن اقامتگاه به تور#
@login_required
def add_tour_accommodation(request, tour_id):

    tour = get_object_or_404(
        Tour,
        id=tour_id
    )

    if request.method == 'POST':

        form = TourAccommodationForm(
            request.POST
        )

        if form.is_valid():

            item = form.save(
                commit=False
            )

            item.tour = tour

            item.save()

            return redirect(
                'dashboard:tour_detail',
                pk=tour.id
            )

    else:

        form = TourAccommodationForm()

    return render(
        request,
        'dashboard/tours/add_accommodation.html',
        {
            'tour': tour,
            'form': form
        }
    )
    
    

#-------------------------------------ویرایش پروازهای تور#
@login_required
def edit_tour_flight(request, pk):

    tour_flight = get_object_or_404(
        TourFlight,
        pk=pk
    )

    if request.method == 'POST':

        form = TourFlightForm(
            request.POST,
            instance=tour_flight
        )

        if form.is_valid():

            form.save()

            return redirect(
                'dashboard:tour_detail',
                pk=tour_flight.tour.id
            )

    else:

        form = TourFlightForm(
            instance=tour_flight
        )

    return render(
        request,
        'dashboard/tours/edit_flight.html',
        {
            'form': form,
            'tour_flight': tour_flight
        }
    )
    
    
    
#--------------------------------------حذف پروازهای تور#
@login_required
def delete_tour_flight(request, pk):

    tour_flight = get_object_or_404(
        TourFlight,
        pk=pk
    )

    tour_id = tour_flight.tour.id

    tour_flight.delete()

    return redirect(
        'dashboard:tour_detail',
        pk=tour_id
    )
    
    
    
#---------------------------------------ویرایش اقامتگاهای تور#
@login_required
def edit_tour_accommodation(request, pk):

    item = get_object_or_404(
        TourAccommodation,
        pk=pk
    )

    if request.method == 'POST':

        form = TourAccommodationForm(
            request.POST,
            instance=item
        )

        if form.is_valid():

            form.save()

            return redirect(
                'dashboard:tour_detail',
                pk=item.tour.id
            )

    else:

        form = TourAccommodationForm(
            instance=item
        )

    return render(
        request,
        'dashboard/tours/edit_accommodation.html',
        {
            'form': form,
            'item': item
        }
    )
    
    
#-----------------------------------------حذف اقامتگاهای تور#
@login_required
def delete_tour_accommodation(request, pk):

    item = get_object_or_404(
        TourAccommodation,
        pk=pk
    )

    tour_id = item.tour.id

    item.delete()

    return redirect(
        'dashboard:tour_detail',
        pk=tour_id
    )
    
    
    
#---------------------------------------------لیست کشورها#
@login_required
def country_list(request):

    countries = Country.objects.all().order_by(
        'name'
    )

    return render(
        request,
        'dashboard/countries/list.html',
        {
            'countries': countries
        }
    )
    
    
    
#------------------------------------------------افزودن کشور#
@login_required
def add_country(request):

    if request.method == 'POST':

        form = CountryForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect(
                'dashboard:country_list'
            )

    else:

        form = CountryForm()

    return render(
        request,
        'dashboard/countries/add.html',
        {
            'form': form
        }
    )
    
    
#------------------------------------------ویرایش کشورها #
@login_required
def edit_country(request, pk):

    country = get_object_or_404(
        Country,
        pk=pk
    )

    if request.method == 'POST':

        form = CountryForm(
            request.POST,
            instance=country
        )

        if form.is_valid():

            form.save()

            return redirect(
                'dashboard:country_list'
            )

    else:

        form = CountryForm(
            instance=country
        )

    return render(
        request,
        'dashboard/countries/edit.html',
        {
            'form': form
        }
    )
    
    
    
    
#-------------------------------------------حذف کشورها#
@login_required
def delete_country(request, pk):

    country = get_object_or_404(
        Country,
        pk=pk
    )

    try:

        country.delete()

    except Exception:

        messages.error(
            request,
            'این کشور در سیستم استفاده شده است'
        )

    return redirect(
        'dashboard:country_list'
    )
    
    
#--------------------------------------------لیست شهرها#
@login_required
def city_list(request):

    cities = City.objects.select_related(
        'country'
    )

    return render(
        request,
        'dashboard/cities/list.html',
        {
            'cities': cities
        }
    )
    
    

#---------------------------------------------افزودن شهرها#
@login_required
def add_city(request):

    if request.method == 'POST':

        form = CityForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect(
                'dashboard:city_list'
            )

    else:

        form = CityForm()

    return render(
        request,
        'dashboard/cities/add.html',
        {
            'form': form
        }
    )
    
    
    
#-----------------------------------------ویرایش شهرها#
@login_required
def edit_city(request, pk):

    city = get_object_or_404(
        City,
        pk=pk
    )

    if request.method == 'POST':

        form = CityForm(
            request.POST,
            instance=city
        )

        if form.is_valid():

            form.save()

            return redirect(
                'dashboard:city_list'
            )

    else:

        form = CityForm(
            instance=city
        )

    return render(
        request,
        'dashboard/cities/edit.html',
        {
            'form': form
        }
    )
    
    
    
#--------------------------------------------حذف شهرها#
@login_required
def delete_city(request, pk):

    city = get_object_or_404(
        City,
        pk=pk
    )

    try:

        city.delete()

    except Exception:

        messages.error(
            request,
            'این شهر در سیستم استفاده شده است'
        )

    return redirect(
        'dashboard:city_list'
    )
    
 
 
#-----------------------------------------------لیست استرداد #
@login_required
def refund_list(request):

    refunds = Refund.objects.select_related(
        'booking_item',
        'booking_item__booking'
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'dashboard/bookings/refund_list.html',
        {
            'refunds': refunds
        }
    )
    
    
#--------------------------------------اضافه کردن کنسلی ها#
@login_required
def add_refund(request, pk):

    booking_item = get_object_or_404(
        BookingItem,
        pk=pk
    )

    if request.method == 'POST':

        form = RefundForm(
            request.POST
        )

        if form.is_valid():

            refund = form.save(
                commit=False
            )

            refund.booking_item = booking_item

            refund.save()

            return redirect(
                'dashboard:booking_detail',
                pk=booking_item.booking.id
            )

    else:

        form = RefundForm()

    return render(
        request,
        'dashboard/bookings/add_refund.html',
        {
            'form': form,
            'booking_item': booking_item
        }
    )
    
    
    
    
#------------------------------------------------ویرایش کنسلی ها#
@login_required
def edit_refund(request, pk):

    refund = get_object_or_404(
        Refund,
        pk=pk
    )

    if request.method == 'POST':

        form = RefundForm(
            request.POST,
            instance=refund
        )

        if form.is_valid():

            form.save()

            return redirect(
                'dashboard:booking_detail',
                pk=refund.booking_item.booking.id
            )

    else:

        form = RefundForm(
            instance=refund
        )

    return render(
        request,
        'dashboard/bookings/edit_refund.html',
        {
            'form': form,
            'refund': refund
        }
    )
    
    
    
#---------------------------------------------حذف کنسلی#
@login_required
def delete_refund(request, pk):

    refund = get_object_or_404(
        Refund,
        pk=pk
    )

    booking_id = refund.booking_item.booking.id

    if request.method == 'POST':

        refund.delete()

        return redirect(
            'dashboard:booking_detail',
            pk=booking_id
        )

    return render(
        request,
        'dashboard/bookings/delete_refund.html',
        {
            'refund': refund
        }
    )
    
    
    
    

#---------------------------------------ثبت هزینه در رزرو#
@login_required
def add_booking_expense(request, booking_id):

    booking = get_object_or_404(
        Booking,
        pk=booking_id
    )

    if request.method == 'POST':

        form = ExpenseForm(
            request.POST
        )

        if form.is_valid():

            expense = form.save(
                commit=False
            )

            expense.booking = booking

            expense.save()

            return redirect(
                'dashboard:booking_detail',
                pk=booking.id
            )

    else:

        form = ExpenseForm()

    return render(
        request,
        'dashboard/expenses/add_booking_expense.html',
        {
            'form': form,
            'booking': booking
        }
    )



    
    
#--------------------------------------------لیست هزینه ها#

@login_required
def expense_list(request):

    expenses = Expense.objects.select_related(
        'booking'
    ).order_by(
        '-paid_at'
    )

    return render(
        request,
        'dashboard/expenses/list.html',
        {
            'expenses': expenses
        }
    )






    
#---------------------------------------ثبت و اضافه کردن هزینه#
@login_required
def add_expense(request):

    if request.method == 'POST':

        form = ExpenseForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            return redirect(
                'dashboard:expense_list'
            )

    else:

        form = ExpenseForm()

    return render(
        request,
        'dashboard/expenses/add.html',
        {
            'form': form
        }
    )
    
    
    
#-------------------------------------------------ویرایش هزینه#

@login_required
def edit_expense(request, pk):

    expense = get_object_or_404(
        Expense,
        pk=pk
    )

    if request.method == 'POST':

        form = ExpenseForm(
            request.POST,
            instance=expense
        )

        if form.is_valid():

            form.save()

            return redirect(
                'dashboard:expense_list'
            )

    else:

        form = ExpenseForm(
            instance=expense
        )

    return render(
        request,
        'dashboard/expenses/edit.html',
        {
            'form': form,
            'expense': expense
        }
    )
    
    
#--------------------------------------------------حذف هزینه ها#
@login_required
def delete_expense(request, pk):

    expense = get_object_or_404(
        Expense,
        pk=pk
    )

    if request.method == 'POST':

        expense.delete()

        return redirect(
            'dashboard:expense_list'
        )

    return render(
        request,
        'dashboard/expenses/delete.html',
        {
            'expense': expense
        }
    )
    
    
    
    
    
#---------------------------------------------افزودن مدارک#
@login_required
def add_document(request, passenger_id):

    passenger = get_object_or_404(
        Passenger,
        pk=passenger_id
    )

    if request.method == 'POST':

        form = DocumentForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            document = form.save(
                commit=False
            )

            document.passenger = passenger

            document.save()

            return redirect(
                'dashboard:passenger_detail',
                pk=passenger.id
            )

    else:

        form = DocumentForm()

    return render(
        request,
        'dashboard/passengers/add_document.html',
        {
            'form': form,
            'passenger': passenger
        }
    )
    
    
    
    
    
#----------------------------------------------------ویرایش مدارک#

@login_required
def edit_document(request, pk):

    document = get_object_or_404(
        Document,
        pk=pk
    )

    if request.method == 'POST':

        form = DocumentForm(
            request.POST,
            request.FILES,
            instance=document
        )

        if form.is_valid():

            form.save()

            return redirect(
                'dashboard:passenger_detail',
                pk=document.passenger.id
            )

    else:

        form = DocumentForm(
            instance=document
        )

    return render(
        request,
        'dashboard/documents/edit.html',
        {
            'form': form,
            'document': document
        }
    )
    
    
    
    
#----------------------------------------------حذف مدارک#

@login_required
def delete_document(request, pk):

    document = get_object_or_404(
        Document,
        pk=pk
    )

    passenger_id = document.passenger.id

    if request.method == 'POST':

        if document.file:
            document.file.delete(
                save=False
            )

        document.delete()

        return redirect(
            'dashboard:passenger_detail',
            pk=passenger_id
        )

    return render(
        request,
        'dashboard/documents/delete.html',
        {
            'document': document
        }
    )
    
    

#---------------------------------------------ثبت پایپورت#

@login_required
def add_passport(request, passenger_id):

    passenger = get_object_or_404(
        Passenger,
        pk=passenger_id
    )

    if hasattr(passenger, 'passport'):

        return redirect(
            'dashboard:edit_passport',
            pk=passenger.passport.id
        )

    if request.method == 'POST':

        form = PassportForm(
            request.POST
        )

        if form.is_valid():

            passport = form.save(
                commit=False
            )

            passport.passenger = passenger

            passport.save()

            return redirect(
                'dashboard:passenger_detail',
                pk=passenger.id
            )

    else:

        form = PassportForm()

    return render(
        request,
        'dashboard/passports/add.html',
        {
            'form': form,
            'passenger': passenger
        }
    )
    
    
    
#----------------------------------------------ویرایش پاسپورت#
@login_required
def edit_passport(request, pk):

    passport = get_object_or_404(
        Passport,
        pk=pk
    )

    if request.method == 'POST':

        form = PassportForm(
            request.POST,
            instance=passport
        )

        if form.is_valid():

            form.save()

            return redirect(
                'dashboard:passenger_detail',
                pk=passport.passenger.id
            )

    else:

        form = PassportForm(
            instance=passport
        )

    return render(
        request,
        'dashboard/passports/edit.html',
        {
            'form': form,
            'passport': passport
        }
    )
    
    
    
#----------------------------------------------------حذف پاسپورت#

@login_required
def delete_passport(request, pk):

    passport = get_object_or_404(
        Passport,
        pk=pk
    )

    passenger_id = passport.passenger.id

    if request.method == 'POST':

        passport.delete()

        return redirect(
            'dashboard:passenger_detail',
            pk=passenger_id
        )

    return render(
        request,
        'dashboard/passports/delete.html',
        {
            'passport': passport
        }
    )
    
    




#------------------------------------------------گزارش مالی#

@login_required
def financial_report(request):
    
    from_date = request.GET.get(
        'from_date'
        )

    to_date = request.GET.get(
        'to_date'
    )

    bookings = Booking.objects.prefetch_related(
        'items',
        'payments'
    )

    if from_date:

        bookings = bookings.filter(
            created_at__date__gte=from_date
        )

    if to_date:

        bookings = bookings.filter(
            created_at__date__lte=to_date
        )

    total_revenue = 0
    total_received = 0
    total_debt = 0

    for booking in bookings:

        total_revenue += booking.actual_total_price

        total_received += booking.paid_amount

        total_debt += booking.remaining_amount
        

    expenses = Expense.objects.all()

    if from_date:

        expenses = expenses.filter(
            paid_at__gte=from_date
        )

    if to_date:

        expenses = expenses.filter(
            paid_at__lte=to_date
        )

    total_expenses = expenses.aggregate(
        total=Sum('amount')
    )['total'] or 0

    total_profit = ( total_revenue- total_expenses)

    debtors = [booking
    for booking in bookings
    if booking.remaining_amount > 0
    ]

    debtor_count = len(debtors)

    largest_debt = 0

    for booking in debtors:

        if booking.remaining_amount > largest_debt:

            largest_debt = booking.remaining_amount
    
    
    
    
    today = date.today()

    today_revenue = 0
    month_revenue = 0
    year_revenue = 0

    for booking in bookings:

        booking_date = booking.created_at.date()

        if booking_date == today:
            today_revenue += booking.actual_total_price

        if (
            booking_date.month == today.month and
            booking_date.year == today.year
        ):
            month_revenue += booking.actual_total_price

        if booking_date.year == today.year:
            year_revenue += booking.actual_total_price


    top_debtor = None

    if debtors:

        top_debtor = max(
            debtors,
            key=lambda x: x.remaining_amount
        )


    tour_count = BookingItem.objects.filter(
        item_type='tour'
    ).count()

    flight_count = BookingItem.objects.filter(
        item_type='flight'
    ).count()

    accommodation_count = BookingItem.objects.filter(
        item_type='accommodation'
    ).count()

    visa_count = BookingItem.objects.filter(
        item_type='visa'
    ).count()


    service_stats = {

        'تور': tour_count,
        'پرواز': flight_count,
        'اقامتگاه': accommodation_count,
        'ویزا': visa_count,

    }

    best_service = max(
        service_stats,
        key=service_stats.get
    )
    
    
    booking_profits = []

    for booking in bookings:

        booking_expenses = booking.expenses.aggregate(
            total=Sum('amount')
        )['total'] or 0

        booking_profit = (
            booking.actual_total_price
            - booking_expenses
        )

        booking_profits.append({

            'booking': booking,

            'revenue': booking.actual_total_price,

            'expense': booking_expenses,

            'profit': booking_profit,

        })
    
    context = {

        'total_revenue': total_revenue,

        'total_received': total_received,

        'total_debt': total_debt,

        'total_expenses': total_expenses,

        'total_profit': total_profit,

        'debtors': debtors,
        
        'debtor_count': debtor_count,

        'largest_debt': largest_debt,
        
        'today_revenue': today_revenue,

        'month_revenue': month_revenue,

        'year_revenue': year_revenue,

        'top_debtor': top_debtor,

        'best_service': best_service,
        
        'from_date': from_date,

        'to_date': to_date,
        
        'booking_profits': booking_profits,

    }

    return render(
        request,
        'dashboard/reports/financial_report.html',
        context
    )
    
    
    
    
#------------------------------------------------خروجی گزارش اکسل#    
    
@login_required
def financial_report_excel(request):

    bookings = Booking.objects.prefetch_related(
        'items',
        'payments'
    )

    wb = Workbook()

    ws = wb.active

    ws.title = "Financial Report"

    ws.append([

        'کد رزرو',

        'مسافر',

        'درآمد',

        'هزینه',

        'سود',

        'بدهی',

    ])

    for booking in bookings:

        booking_expenses = booking.expenses.aggregate(
            total=Sum('amount')
        )['total'] or 0

        booking_profit = (
            booking.actual_total_price
            - booking_expenses
        )

        ws.append([

            booking.booking_code,

            str(booking.passenger),

            booking.actual_total_price,

            booking_expenses,

            booking_profit,

            booking.remaining_amount,

        ])

    response = HttpResponse(

        content_type=
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

    )

    response['Content-Disposition'] = (
        'attachment; filename=financial_report.xlsx'
    )

    wb.save(response)

    return response