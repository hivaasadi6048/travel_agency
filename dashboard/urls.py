from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
path('', views.dashboard_view, name='dashboard'),
    
    path('payments/',views.payment_list, name='payment_list'),
        
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    

    path('passengers/', views.passenger_list, name='passengers'),
    path('passengers/<int:pk>/',views.passenger_detail,name='passenger_detail'),
    path('passengers/<int:pk>/add-payment/',views.add_payment,name='add_payment'),
    path('passengers/create/',views.passenger_create,name='passenger_create'),
    path('passengers/<int:pk>/edit/',views.passenger_edit,name='passenger_edit'),
    path('passengers/<int:pk>/delete/',views.delete_passenger,name='delete_passenger'),
  
    path('bookings/',views.bookings_list, name='bookings'),
    path('bookings/create/',views.booking_create,name='booking_create'),
    path('bookings/<int:pk>/delete/',views.delete_booking,name='delete_booking'),
    path('bookings/<int:pk>/',views.booking_detail,name='booking_detail'),
    path('bookings/<int:booking_id>/add-tour/',views.add_tour_to_booking,name='add_tour_to_booking'),
    path('bookings/<int:booking_id>/add-flight/',views.add_flight_to_booking,name='add_flight_to_booking'),
    path('bookings/<int:booking_id>/add-visa/',views.add_visa_to_booking,name='add_visa_to_booking'),
    path('bookings/<int:booking_id>/add-accommodation/',views.add_accommodation_to_booking,name='add_accommodation_to_booking'),
    path('booking-items/<int:pk>/delete/',views.delete_booking_item,name='delete_booking_item'),
    path('booking-items/<int:pk>/edit/',views.edit_booking_item,name='edit_booking_item'),
    path('bookings/<int:pk>/edit/',views.edit_booking,name='edit_booking'),
    
    
    path('accommodations/',views.accommodation_list,name='accommodation_list'),
    path('accommodations/add/',views.add_accommodation,name='add_accommodation'),
    path('accommodations/<int:pk>/edit/',views.edit_accommodation,name='edit_accommodation'),
    path('accommodations/<int:pk>/delete/',views.delete_accommodation, name='delete_accommodation'),
    
    
    path('visas/',views.visa_list,name='visa_list'),   
    path('visas/add/',views.add_visa,name='add_visa'),
    path('visas/<int:pk>/edit/',views.edit_visa,name='edit_visa'),
    path('visas/<int:pk>/delete/',views.delete_visa,name='delete_visa'),
    
    
    path('flights/',views.flight_list,name='flight_list'),
    path('flights/add/',views.add_flight,name='add_flight'),
    path('flights/<int:pk>/edit/',views.edit_flight,name='edit_flight'),
    path('flights/<int:pk>/delete/',views.delete_flight,name='delete_flight'),
    
    
    path('tours/',views.tour_list,name='tour_list'),
    path('tours/add/',views.add_tour,name='add_tour'),
    path('tours/<int:pk>/edit/',views.edit_tour,name='edit_tour'),
    path('tours/<int:pk>/delete/',views.delete_tour,name='delete_tour'),
    
    
    path('tours/<int:pk>/',views.tour_detail,name='tour_detail'),
    path('tours/<int:tour_id>/add-flight/',views.add_tour_flight,name='add_tour_flight'),
    path('tours/<int:tour_id>/add-accommodation/',views.add_tour_accommodation,name='add_tour_accommodation'),
    path('tour-flights/<int:pk>/edit/',views.edit_tour_flight,name='edit_tour_flight'),
    path('tour-flights/<int:pk>/delete/',views.delete_tour_flight,name='delete_tour_flight'),
    path('tour-accommodations/<int:pk>/edit/',views.edit_tour_accommodation,name='edit_tour_accommodation'),
    path('tour-accommodations/<int:pk>/delete/',views.delete_tour_accommodation,name='delete_tour_accommodation'),
    
    
    path('countries/',views.country_list,name='country_list'),
    path('countries/add/',views.add_country,name='add_country'),
    path('countries/<int:pk>/edit/',views.edit_country,name='edit_country'),
    path('countries/<int:pk>/delete/',views.delete_country,name='delete_country'),
    
    
    path('cities/',views.city_list,name='city_list'),
    path('cities/add/',views.add_city,name='add_city'),
    path('cities/<int:pk>/edit/',views.edit_city,name='edit_city'),
    path('cities/<int:pk>/delete/',views.delete_city,name='delete_city'),
    
    
    path('booking-item/<int:pk>/refund/',views.add_refund,name='add_refund'),
    path('refunds/',views.refund_list,name='refund_list'),
    path('refunds/<int:pk>/edit/',views.edit_refund,name='edit_refund'),
    path('refunds/<int:pk>/delete/',views.delete_refund,name='delete_refund'),
    
    
    path('reports/financial/',views.financial_report,name='financial_report'),
    path('reports/financial/excel/',views.financial_report_excel,name='financial_report_excel'),
    
    path('search/',views.global_search,name='global_search'),
    
    path('expenses/',views.expense_list,name='expense_list'),
    path('expenses/add/',views.add_expense,name='add_expense'),
    path('expenses/<int:pk>/edit/',views.edit_expense,name='edit_expense'),
    path('expenses/<int:pk>/delete/',views.delete_expense,name='delete_expense'),
    path('bookings/<int:booking_id>/add-expense/',views.add_booking_expense,name='add_booking_expense'),
    
    
    path('passengers/<int:passenger_id>/passport/add/',views.add_passport,name='add_passport'),
    path('passports/<int:pk>/edit/',views.edit_passport,name='edit_passport'),
    path('passports/<int:pk>/delete/',views.delete_passport,name='delete_passport'),
    
    
    path('documents/<int:pk>/edit/',views.edit_document,name='edit_document'),
    path('documents/<int:pk>/delete/',views.delete_document,name='delete_document'),
    path('passengers/<int:passenger_id>/documents/add/',views.add_document,name='add_document'),

    ]
