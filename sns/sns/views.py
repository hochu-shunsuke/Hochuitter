from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_invalid(self, form):
        error_messages = {
            '__all__': {
                'invalid_login': 'ログインに失敗しました。ユーザー名とパスワードを確認してください。',
                'inactive': 'このアカウントは現在無効になっています。',
            },
            'username': {
                'required': 'ユーザー名を入力してください。',
                'invalid': '有効なユーザー名を入力してください。',
                'max_length': 'ユーザー名は150文字以下である必要があります。',
            },
            'password': {
                'required': 'パスワードを入力してください。',
                'invalid': '有効なパスワードを入力してください。',
            }
        }

        default_messages = {
            'required': 'この項目は必須です。',
            'invalid': '入力内容が正しくありません。'
        }

        for field, errors in form.errors.items():
            for error in errors:
                # フィールド固有のエラーメッセージを確認
                field_messages = error_messages.get(field, {})
                error_key = next((k for k in field_messages if k in error.lower()), None)

                if error_key:
                    messages.error(self.request, field_messages[error_key])
                else:
                    # 一般的なエラーメッセージを確認
                    default_key = next((k for k in default_messages if k in error.lower()), None)
                    if default_key:
                        messages.error(self.request, default_messages[default_key])
                    else:
                        # どのパターンにも一致しない場合はデフォルトメッセージ
                        messages.error(self.request, 'ログインに問題が発生しました。入力内容を確認してください。')

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
                'invalid': '有効なアカウント名を入力してください。',
                'max_length': 'アカウント名は150文字以下である必要があります。'
            },
            'password1': {
                'required': 'パスワードを入力してください。',
                'password_too_short': 'パスワードは最低8文字以上必要です。',
                'password_too_common': 'このパスワードは一般的すぎます。より複雑なパスワードを設定してください。',
                'password_entirely_numeric': 'パスワードを数字だけにすることはできません。',
                'password_too_similar': 'パスワードがアカウント名と似すぎています。'
            },
            'password2': {
                'required': '確認用パスワードを入力してください。',
                'password_mismatch': '入力された2つのパスワードが一致しません。もう一度入力してください。'
            }
        }

        default_messages = {
            'email': 'メールアドレスの形式が正しくありません。',
            'invalid': '入力内容が正しくありません。',
            'required': 'この項目は必須です。',
            'unique': 'この値は既に使用されています。',
            'max_length': '入力が長すぎます。',
            'min_length': '入力が短すぎます。'
        }

        for field, errors in form.errors.items():
            for error in errors:
                # まず、フィールド固有のエラーメッセージを確認
                field_messages = error_messages.get(field, {})
                error_key = next((k for k in field_messages if k in error.lower()), None)
                
                if error_key:
                    messages.error(self.request, field_messages[error_key])
                else:
                    # 一般的なエラーメッセージを確認
                    default_key = next((k for k in default_messages if k in error.lower()), None)
                    if default_key:
                        messages.error(self.request, default_messages[default_key])
                    else:
                        # どのパターンにも一致しない場合は、一般的なエラーメッセージ
                        messages.error(self.request, '入力内容に問題があります。')

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
