from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            if field == '__all__':
                messages.error(self.request, 'ユーザー名またはパスワードが正しくありません。')
            elif field == 'username':
                messages.error(self.request, 'ユーザー名を入力してください。')
            elif field == 'password':
                messages.error(self.request, 'パスワードを入力してください。')
        return super().form_invalid(form)

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = '/'

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, '登録が完了しました。')
        return response

    def form_invalid(self, form):
        error_messages = {
            'username': {
                'unique': 'このアカウント名は既に使用されています。別のアカウント名を入力してください。',
                'required': 'アカウント名を入力してください。',
                'invalid': '有効なアカウント名を入力してください。'
            },
            'password1': {
                'required': 'パスワードを入力してください。',
                'password_too_short': 'パスワードは最低8文字以上必要です。',
                'password_too_common': 'このパスワードは一般的すぎます。より複雑なパスワードを設定してください。',
                'password_entirely_numeric': 'パスワードを数字だけにすることはできません。',
            },
            'password2': {
                'required': '確認用パスワードを入力してください。',
                'password_mismatch': '入力された2つのパスワードが一致しません。もう一度入力してください。'
            }
        }

        for field, errors in form.errors.items():
            for error in errors:
                error_key = next((k for k in error_messages.get(field, {}) if k in error.lower()), None)
                if error_key:
                    messages.error(self.request, error_messages[field][error_key])
                else:
                    messages.error(self.request, error)

        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['password_requirements'] = [
            'パスワードは8文字以上である必要があります',
            '一般的なパスワードは使用できません',
            '数字だけのパスワードは使用できません',
            'パスワードは2回同じものを入力してください'
        ]
        return context
