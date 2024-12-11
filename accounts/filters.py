import django_filters
from . models import CustomUser
from restaurant.models import Restaurant
from restaurant.models import Category

class CustomUserFilter(django_filters.FilterSet):
    #name = django_filters.CharFilter(lookup_expr='iexact')
    class Meta:
        model = CustomUser
        fields = ['email']
        
class RestaurantFilter(django_filters.FilterSet):
    #name = django_filters.CharFilter(lookup_expr='iexact')
    class Meta:
        model = Restaurant
        fields = ['name']
        
class CategoryFilter(django_filters.FilterSet):
    #name = django_filters.CharFilter(lookup_expr='iexact')
    class Meta:
        model = Category
        fields = ['name']