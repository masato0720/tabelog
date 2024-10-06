from django.contrib import admin

from .models import Category, Favorite, Reservation, Restaurant, Review

admin.site.register(Category)
admin.site.register(Restaurant)
admin.site.register(Reservation)
admin.site.register(Review)
admin.site.register(Favorite)
