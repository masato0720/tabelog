from django.urls import path

from . import views


urlpatterns = [
    path("user-detail/<int:pk>/", views.UserDetailView.as_view(), name="user_detail"),
    path("user-update/<int:pk>/", views.UserUpdateView.as_view(), name="user_update"),
    
   
    path('management_user', 
         views.userList,
         name='management_user',
    ),
    path('management_shop', 
         views.shopList,
         name='management_shop',
    ),
    path('management_category', 
         views.categoryList,
         name='management_category',
    ),
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
