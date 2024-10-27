import stripe
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse

from django.shortcuts import redirect, render, get_object_or_404


from django.urls import reverse_lazy
from django.views import View, generic

from . import forms, models
from . models import CustomUser
from restaurant.models import Restaurant
from restaurant.models import Category



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


class SubscribeRegisterView(View):
    template = "subscribe/subscribe_register.html"

    def get(self, request):
        context = {}
        return render(self.request, self.template, context)

    def post(self, request):
        user_id = request.user.id
        card_name = request.POST.get("card_name")
        card_number = request.POST.get("card_number")
        correct_cord_number = "4242424242424242"

        if card_number != correct_cord_number:
            context = {"error_message": "クレジットカード番号が正しくありません"}
            return render(self.request, self.template, context)

        models.CustomUser.objects.filter(id=user_id).update(
            is_subscribed=True, card_name=card_name, card_number=card_number
        )

        return redirect(reverse_lazy("top_page"))


class SubscribeCancelView(generic.TemplateView):
    template_name = "subscribe/subscribe_cancel.html"

    def post(self, request):
        user_id = request.user.id

        models.CustomUser.objects.filter(id=user_id).update(is_subscribed=False)

        return redirect(reverse_lazy("top_page"))


class SubscribePaymentView(View):
    template = "subscribe/subscribe_payment.html"

    def get(self, request):
        user_id = request.user.id
        user = models.CustomUser.objects.get(id=user_id)
        context = {"user": user}
        return render(self.request, self.template, context)

    def post(self, request):
        user_id = request.user.id
        card_name = request.POST.get("card_name")
        card_number = request.POST.get("card_number")
        print(card_name, card_number)

        models.CustomUser.objects.filter(id=user_id).update(
            card_name=card_name, card_number=card_number
        )
        return redirect(reverse_lazy("top_page"))



# 管理画面 
# ユーザー一覧画面  
def userList(request):
    deta = models.CustomUser.objects.all()
    params = {
       'title': '会員管理',
       'message': 'all user',
       'data': deta,
    }
    return render(request,'management/management_user.html',params)   

# 店舗一覧画面  
def shopList(request):
    deta = Restaurant.objects.all()
    params = {
       'title': '店舗管理',
       'message': 'all shop',
       'data': deta,
    }
    return render(request,'management/management_shop.html',params)  

# カテゴリー一覧画面  
def categoryList(request):
    deta = Category.objects.all()
    params = {
       'title': 'カテゴリー管理',
       'message': 'all category',
       'data': deta,
    }
    return render(request,'management/management_category.html',params)  

    
    

# Stripe APIキーを設定
stripe.api_key = settings.STRIPE_SECRET_KEY

# Stripeの支払いview
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
            success_url=f"{settings.YOUR_DOMAIN}/checkout_success/?session_id={{CHECKOUT_SESSION_ID}}&user_id={request.user.id}",
            cancel_url=f"{settings.YOUR_DOMAIN}/checkout_cancel/",
        )
        return redirect(checkout_session.url, code=303)
    
    #successの戻るurls.pyを作成する
    #cancelの戻るurls.pyを作成する
    #gitにアップして先生にコードを見てもらう
    #管理画面のログインは管理者フラグがデフォルトであるのでそれを活用する。


# 支払い成功（会員のみ）
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
        user.save()

        return render(request, 'subscription/subscription_register.html')
    


# サブスク案内（有料会員以外）
class SubscriptionGuideView(generic.TemplateView):
    template_name = "subscription/subscription_register.html"




    

