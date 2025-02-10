from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
import logging

logger = logging.getLogger(__name__)

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_invalid(self, form):
        """
        ログインフォームが無効な場合の処理。
        エラーメッセージを表示してログインページにリダイレクト。
        """
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
        """
        フォームが有効な場合の処理。
        ユーザーを登録し、自動的にログインさせる。
        """
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, '登録が完了しました。')
        return response

    def form_invalid(self, form):
        """
        フォームが無効な場合の処理。
        各フィールドのエラーを解析し、適切なメッセージを表示。
        """
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

        # エラーを解析してメッセージを生成
        for field, errors in form.errors.items():
            for error in errors:
                logger.debug(f"Field: {field}, Error: {error}")  # デバッグ用ログ

                # まず、フィールド固有のエラーメッセージを確認
                field_messages = error_messages.get(field, {})
                matched_error_key = None

                # エラーコードを正確にマッチさせる
                for key in field_messages.keys():
                    if key in error.lower():
                        matched_error_key = key
                        break

                if matched_error_key:
                    messages.error(self.request, field_messages[matched_error_key])
                else:
                    # 一般的なエラーメッセージを確認
                    default_key = next((k for k in default_messages if k in error.lower()), None)
                    if default_key:
                        messages.error(self.request, default_messages[default_key])
                    else:
                        # どのパターンにも一致しない場合は、エラー内容をそのまま表示
                        messages.error(self.request, f" {error}")

        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        """
        コンテキストデータを追加。
        パスワード要件やフォームエラーをテンプレートに渡す。
        """
        context = super().get_context_data(**kwargs)
        context['password_requirements'] = [
            'パスワードは8文字以上である必要があります',
            '一般的なパスワードは使用できません',
            '数字だけのパスワードは使用できません',
            'パスワードは2回同じものを入力してください'
        ]

        # フォームエラーをコンテキストに追加
        if self.request.method == 'POST':
            context['form_errors'] = self.get_form().errors

        return context