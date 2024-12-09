import django_filters
from . models import CustomUser

class ShopFilter(django_filters.FilterSet):
    #name = django_filters.CharFilter(lookup_expr='iexact')
    class Meta:
        model = CustomUser
        fields = ['email']