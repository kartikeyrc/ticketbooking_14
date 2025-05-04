from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Avg
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, View
from django.urls import reverse_lazy
from django import forms
from .models import Show, Booking, Rating
from decimal import Decimal

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class IndexView(TemplateView):
    template_name = 'booking/index.html'

class RegisterView(CreateView):
    template_name = 'booking/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('booking:show_list')

    def form_valid(self, form):
        password1 = self.request.POST.get('password1')
        password2 = self.request.POST.get('password2')
        
        if password1 != password2:
            form.add_error(None, 'Passwords do not match')
            return self.form_invalid(form)
        
        if User.objects.filter(username=form.cleaned_data['username']).exists():
            form.add_error('username', 'Username already exists')
            return self.form_invalid(form)
        
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        login(self.request, user)
        return super().form_valid(form)

class LoginView(View):
    template_name = 'booking/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('booking:show_list')
        else:
            return render(request, self.template_name, {'error': 'Invalid username or password'})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('booking:login')

class ShowListView(ListView):
    model = Show
    template_name = 'booking/show_list.html'
    context_object_name = 'shows'

    def get_queryset(self):
        return Show.objects.annotate(
            average_rating=Avg('ratings__rating')
        ).all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for show in context['shows']:
            show.user_can_rate = False
            if self.request.user.is_authenticated:
                has_booking = Booking.objects.filter(
                    user=self.request.user,
                    show=show,
                    status='COMPLETED'
                ).exists()
                has_rated = Rating.objects.filter(
                    user=self.request.user,
                    show=show
                ).exists()
                show.user_can_rate = has_booking and not has_rated
        return context

class BookShowView(LoginRequiredMixin, View):
    template_name = 'booking/book_show.html'

    def get(self, request, show_id):
        show = get_object_or_404(Show, id=show_id)
        return render(request, self.template_name, {'show': show})

    def post(self, request, show_id):
        show = get_object_or_404(Show, id=show_id)
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

class RateShowView(LoginRequiredMixin, View):
    def post(self, request, show_id):
        show = get_object_or_404(Show, id=show_id)
        
        has_booking = Booking.objects.filter(
            user=request.user,
            show=show,
            status='COMPLETED'
        ).exists()
        
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

class BookingHistoryView(LoginRequiredMixin, ListView):
    template_name = 'booking/booking_history.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-booking_time')

class CancelBookingView(LoginRequiredMixin, View):
    def get(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        
        if booking.status == 'PENDING':
            booking.status = 'CANCELLED'
            booking.save()
            
            booking.show.booked_seats -= booking.number_of_tickets
            booking.show.save()
            
            messages.success(request, 'Booking cancelled successfully!')
        
        return redirect('booking:booking_history') 
