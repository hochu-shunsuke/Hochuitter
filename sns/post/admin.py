from django.contrib import admin
from .models import Post

# これがPostモデルをadminに登録するコード!!
admin.site.register(Post)