from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from .models import Show, Booking, Rating
from decimal import Decimal

# Create your views here
def index(request):
    return render(request, 'booking/index.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 != password2:
            return render(request, 'booking/register.html', {'error': 'Passwords do not match'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'booking/register.html', {'error': 'Username already exists'})
        
        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        return redirect('booking:show_list')
    
    return render(request, 'booking/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('booking:show_list')
        else:
            return render(request, 'booking/login.html', {'error': 'Invalid username or password'})
    
    return render(request, 'booking/login.html')

def logout_view(request):
    logout(request)
    return redirect('booking:login')

def show_list(request):
    shows = Show.objects.annotate(
        average_rating=Avg('ratings__rating')
    ).all()
    
    # Add a flag to determine if the user can rate each show
    for show in shows:
        show.user_can_rate = False
        if request.user.is_authenticated:
            # User can rate if they have booked and attended the show
            has_booking = Booking.objects.filter(
                user=request.user,
                show=show,
                status='COMPLETED'
            ).exists()
            # Check if user hasn't already rated
            has_rated = Rating.objects.filter(
                user=request.user,
                show=show
            ).exists()
            show.user_can_rate = has_booking and not has_rated

    return render(request, 'booking/show_list.html', {'shows': shows})

@login_required
def book_show(request, show_id):
    show = get_object_or_404(Show, id=show_id)
    if request.method == 'POST':
        try:
            number_of_tickets = int(request.POST.get('number_of_tickets', 0))
            if number_of_tickets <= 0:
                messages.error(request, 'Number of tickets must be greater than zero.')
                return redirect('booking:book_show', show_id=show.id)
            if number_of_tickets <= show.available_seats:
                booking = Booking.objects.create(
                    user=request.user,
                    show=show,
                    number_of_tickets=number_of_tickets,
                    status='PENDING'
                )
                show.booked_seats += number_of_tickets
                show.save()
                messages.success(request, 'Booking successful!')
                return redirect('booking:booking_history')
            else:
                messages.error(request, 'Not enough seats available.')
        except ValueError:
            messages.error(request, 'Invalid number of tickets.')
        return redirect('booking:book_show', show_id=show.id)
    return render(request, 'booking/book_show.html', {'show': show})

@login_required
def rate_show(request, show_id):
    show = get_object_or_404(Show, id=show_id)
    
    # Check if user has booked and attended the show
    has_booking = Booking.objects.filter(
        user=request.user,
        show=show,
        status='COMPLETED'
    ).exists()
    
    # Check if user hasn't already rated
    has_rated = Rating.objects.filter(
        user=request.user,
        show=show
    ).exists()
    
    if not has_booking:
        messages.error(request, 'You can only rate shows you have attended.')
        return redirect('booking:show_list')
    
    if has_rated:
        messages.error(request, 'You have already rated this show.')
        return redirect('booking:show_list')
    
    if request.method == 'POST':
        try:
            rating_value = int(request.POST.get('rating', 0))
            if 1 <= rating_value <= 5:
                Rating.objects.create(
                    user=request.user,
                    show=show,
                    rating=rating_value,
                    comment=request.POST.get('comment', '')
                )
                messages.success(request, 'Thank you for your rating!')
            else:
                messages.error(request, 'Rating must be between 1 and 5.')
        except ValueError:
            messages.error(request, 'Invalid rating value.')
    
    return redirect('booking:show_list')

@login_required
def booking_history(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_time')
    return render(request, 'booking/booking_history.html', {'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.status == 'PENDING':
        booking.status = 'CANCELLED'
        booking.save()
        
        # Return tickets to available seats
        booking.show.booked_seats -= booking.number_of_tickets
        booking.show.save()
        
        messages.success(request, 'Booking cancelled successfully!')
    
    return redirect('booking:booking_history') 