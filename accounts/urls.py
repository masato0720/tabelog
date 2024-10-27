from django.urls import path

from . import views


urlpatterns = [
    path("user-detail/<int:pk>/", views.UserDetailView.as_view(), name="user_detail"),
    path("user-update/<int:pk>/", views.UserUpdateView.as_view(), name="user_update"),
    
   
    path(
        "subscribe-register/",
        views.SubscribeRegisterView.as_view(),
        name="subscribe_register",
    ),
    path(
        "subscribe-cancel/",
        views.SubscribeCancelView.as_view(),
        name="subscribe_cancel",
    ),
    path(
        "subscribe-payment/",
        views.SubscribePaymentView.as_view(),
        name="subscribe_payment",
    ),
    

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
         name = 'subscription_guide')
]
