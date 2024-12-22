from django.contrib import admin
from .models import Post,Comment

# これがPostモデルをadminに登録するコード!!
admin.site.register(Post)
admin.site.register(Comment)