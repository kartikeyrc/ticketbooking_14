from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('', views.show_list, name='show_list'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('book/<int:show_id>/', views.book_show, name='book_show'),
    path('rate/<int:show_id>/', views.rate_show, name='rate_show'),
    path('bookings/', views.booking_history, name='booking_history'),
    path('booking/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
] 