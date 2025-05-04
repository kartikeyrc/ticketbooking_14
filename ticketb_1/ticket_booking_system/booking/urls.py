from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('', views.ShowListView.as_view(), name='show_list'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('book/<int:show_id>/', views.BookShowView.as_view(), name='book_show'),
    path('rate/<int:show_id>/', views.RateShowView.as_view(), name='rate_show'),
    path('bookings/', views.BookingHistoryView.as_view(), name='booking_history'),
    path('booking/<int:booking_id>/cancel/', views.CancelBookingView.as_view(), name='cancel_booking'),
] 
