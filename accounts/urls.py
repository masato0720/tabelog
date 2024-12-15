from django.urls import path

from . import views

from . models import CustomUser


urlpatterns = [
    path("user-detail/<int:pk>/", views.UserDetailView.as_view(), name="user_detail"),
    
    path("user-update/<int:pk>/", views.UserUpdateView.as_view(), name="user_update"),
    
    path("management_user", views.UserList.as_view(model=CustomUser), name="management_user"),

    path('management_shop', views.ShopList.as_view(),name='management_shop',),
    
    path('management_shop_form', views.ShopCreateView.as_view(), name="management_shop_form"),
    
    path('management_shop_update_form/<int:pk>', views.ShopUpdateView.as_view(), name="management_shop_update_form"),
    
    path('management_shop_confirm_delete/<int:pk>', views.ShopDeleteView.as_view(), name="management_shop_confirm_delete"),
    
    path('management_category', views.CategoryList.as_view(),name='management_category',),
    
    path('management_category_form', views.CategoryCreateView.as_view(), name="management_category_form"),
    
    path('management_category_update_form/<int:pk>', views.CategoryUpdateView.as_view(), name="management_category_update_form"),
    
    path('management_category_confirm_delete/<int:pk>', views.CategoryDeleteView.as_view(), name="management_category_confirm_delete"),
    
    path('subscription_register',
         views.CreateCheckoutSessionView.as_view(),
         name='subscription_register'),
    
    path('subscription_guide',
         views.SubscriptionGuideView.as_view(),
         name = 'subscription_guide'),
    
     path('subscription_success/',
          views.CheckoutSuccessView.as_view(),
          name='subscription_success'),
     
     path('subscription_cancel/',
          views.SubscriptioncancelView.as_view(),
          name='subscription_cancel'),
]
