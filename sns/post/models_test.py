#ここはmodelsの構成を単純かつ効率化できないか実験するファイル

from django.db import models

class Post(models.Model):
    content=models.CharField(max_length=280)
    likecount=models.PositiveIntegerField(default=0)
    post_date=models.DateTimeField(auto_now_add=True)
    