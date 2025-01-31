from django.http import HttpRequest
import stripe
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse

from django.shortcuts import redirect, render, get_object_or_404

from django.urls import reverse_lazy
from django.views import View, generic
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


# 定義したモデルの読み込み
from . import forms, models
from . models import CustomUser
from restaurant.models import Restaurant
from restaurant.models import Category

from .filters import CustomUserFilter, RestaurantFilter, CategoryFilter

from .mixins import OnlyManagementUserMixin
        

""" 会員情報================================== """
class UserDetailView(generic.DetailView):
    model = models.CustomUser
    template_name = "user/user_detail.html"


""" 会員情報の更新================================== """
class UserUpdateView(generic.UpdateView):
    model = models.CustomUser
    template_name = "user/user_update.html"
    form_class = forms.UserUpdateForm

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse_lazy("user_detail", kwargs={"pk": pk})

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

"""管理者画面（ユーザー一覧画面）================================== """

class UserList(OnlyManagementUserMixin, ListView):
    template_name = 'management/management_user.html'
    model = CustomUser
    context_object_name = 'results'
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = CustomUserFilter(self.request.GET,
                queryset=self.get_queryset())
        return context
    
    
"""管理者画面（店舗一覧画面）================================== """
class ShopList(OnlyManagementUserMixin, ListView):
    template_name = 'management/management_shop.html'
    model = Restaurant
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = RestaurantFilter(self.request.GET,
                queryset=self.get_queryset())
        return context
    
class ShopCreateView(OnlyManagementUserMixin, CreateView):
    template_name = 'management/management_shop_form.html'
    model = Restaurant
    fields = '__all__'
    
class ShopUpdateView(OnlyManagementUserMixin, UpdateView):
    template_name = 'management/management_shop_update_form.html'
    model = Restaurant
    fields = '__all__'
    
class ShopDeleteView(OnlyManagementUserMixin, DeleteView):
    template_name = 'management/management_shop_confirm_delete.html'
    model = Restaurant
    success_url = reverse_lazy('management_shop')
    

"""管理者画面（カテゴリー一覧画面）================================== """
class CategoryList(OnlyManagementUserMixin, ListView):
    template_name = 'management/management_category.html'
    model = Category
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = CategoryFilter(self.request.GET,
                queryset=self.get_queryset())
        return context
    
class CategoryCreateView(OnlyManagementUserMixin, CreateView):
    template_name = 'management/management_Category_form.html'
    model = Category
    fields = '__all__'
    
class CategoryUpdateView(OnlyManagementUserMixin, UpdateView):
    template_name = 'management/management_Category_update_form.html'
    model = Category
    fields = '__all__'
    
class CategoryDeleteView(OnlyManagementUserMixin, DeleteView):
    template_name = 'management/management_Category_confirm_delete.html'
    model = Category
    success_url = reverse_lazy('management_category') 

"""Stripe APIキーを設定================================== """
stripe.api_key = settings.STRIPE_SECRET_KEY


"""Stripeの支払いview================================== """
class CreateCheckoutSessionView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        # YOUR_DOMAINが開発環境と本番環境で変わるようにsettings.pyに記述
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': 'price_1Q90y5Rx2MJlJEcGeHMLvs04',
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=f"{settings.YOUR_DOMAIN}/accounts/subscription_success/?session_id={{CHECKOUT_SESSION_ID}}&user_id={request.user.id}",
            cancel_url=f"{settings.YOUR_DOMAIN}/accounts/subscription_cancel/",
        )   
        return redirect(checkout_session.url, code=303)
    
    def get(self, request, *args, **kwargs):
        return render(request, 'subscription/subscription_register.html')


"""支払い成功（会員のみ）================================== """
class CheckoutSuccessView(View):
    def get(self, request, *args, **kwargs):    
        session_id = request.GET.get('session_id')
        user_id = request.GET.get('user_id')

        if not session_id or not user_id:
            return HttpResponse("Invalid request", status=400)
        
        # ここで、session_idを使って支払いが成功したかどうかを確認することもできます
        # 例:
        # session = stripe.checkout.Session.retrieve(session_id)
        # if session.payment_status != 'paid':
        #     return HttpResponse("Payment not completed", status=400)

        # ユーザーの subscription 項目を更新
        user = get_object_or_404(CustomUser, id=user_id)
        user.subscription = True
        user.card_name  = user.hurigana
        user.card_number  = '4242424242424242'
        user.save()
        
        return render(request, 'subscription/subscription_register.html')
    

"""サブスク案内（有料会員以外）================================== """
class SubscriptionGuideView(generic.TemplateView):
    template_name = "subscription/subscription_register.html"
    
"""サブスク（支払い完了）================================== """
class SubscriptionsuccessView(generic.TemplateView):
    template_name = "subscription/checkout_success.html"
    
"""サブスク（キャンセル）================================== """
class SubscriptioncancelView(generic.TemplateView):
    template_name = "subscription/checkout_cancel.html"

    def post(self, request):
        user_id = request.user.id
        
        models.CustomUser.objects.filter(id=user_id).update(subscription=False)
        return redirect(reverse_lazy('top_page'))
    
"""サブスク（クレジット情報の編集）================================== """
class SubscribePaymentView(View):
    template = 'subscription/subscribe_payment.html'
    
    def get(self, request):
        user_id = request.user.id
        user = models.CustomUser.objects.get(id=user_id)
        context = {'user': user}
        return render(self.request, self.template, context)
    
    def post(self, request):
        user_id = request.user.id
        card_name = request.POST.get('card_name')
        card_number = request.POST.get('card_number')
        print(card_name, card_number)
        
        models.CustomUser.objects.filter(id=user_id).update(card_name=card_name, card_number=card_number)
        
        return redirect(reverse_lazy('top_page'))

    

