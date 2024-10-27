from django.contrib import admin

from .models import Category, Favorite, Reservation, Restaurant, Review

#admin.site.register(Category)
#admin.site.register(Restaurant)
#admin.site.register(Reservation)
#admin.site.register(Review)
#admin.site.register(Favorite)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name',]
    search_fields = ['name']
    ordering = ['id']
    list_per_page = 20

admin.site.register(Category,CategoryAdmin)

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','category','zip_code','address',]
    search_fields = ['name']
    ordering = ['id']
    list_filter = ['category']
    list_per_page = 20

admin.site.register(Restaurant,RestaurantAdmin)

class ReservationAdmin(admin.ModelAdmin):
    list_display = ['date','time','number_of_people','user','restaurant',]
    search_fields = ['user','restaurant',]
    ordering = ['date']
    list_per_page = 20

admin.site.register(Reservation,ReservationAdmin)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user','restaurant','comment',]
    search_fields = ['user','restaurant',]
    ordering = ['id']
    list_per_page = 20

admin.site.register(Review,ReviewAdmin)

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['id', 'user','restaurant',]
    search_fields = ['user','restaurant',]
    ordering = ['id']
    list_per_page = 20

admin.site.register(Favorite,FavoriteAdmin)