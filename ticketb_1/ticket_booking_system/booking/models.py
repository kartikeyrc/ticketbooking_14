from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from django.db.models import Avg

class Venue(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    capacity = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.name

class Show(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    date = models.DateTimeField()
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        default=Decimal('0.00')
    )
    total_seats = models.PositiveIntegerField(default=0)
    booked_seats = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        default=0
    )
    total_ratings = models.PositiveIntegerField(default=0)
    
    @property
    def available_seats(self):
        return self.total_seats - self.booked_seats

    @property
    def rating(self):
        avg_rating = self.ratings.aggregate(Avg('rating'))['rating__avg']
        return avg_rating if avg_rating else 0.0

    def __str__(self):
        return f"{self.title} - {self.date.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        ordering = ['date']

class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    number_of_tickets = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        default=1
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )
    booking_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    
    def __str__(self):
        return f"Booking {self.id} - {self.user.username} - {self.show.title}"
    
    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.show.price * self.number_of_tickets
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-booking_time']

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'show')

    def __str__(self):
        return f"{self.user.username}'s rating for {self.show.title}"
