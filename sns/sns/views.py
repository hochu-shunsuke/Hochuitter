from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.views.generic.edit import CreateView

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = '/'

    def form_valid(self, form):
        # フォームが有効な場合の処理
        response = super().form_valid(form)
        # 作成したユーザーで自動ログイン
        login(self.request, self.object)
        return response
