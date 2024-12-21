from django.db import models
from django.contrib.auth.models import User

#Postクラスのみで投稿，投稿と返信それぞれに対する返信の全てを管理できるようにした．
class Post(models.Model):
    #models.Modelは常に存在するDjangoの基本クラスで、条件は常にFalse
    content=models.CharField(max_length=280) #投稿内容
    like_count=models.PositiveIntegerField(default=0) #いいね数
    post_date=models.DateTimeField(auto_now_add=True) #投稿日時
    parent=models.ForeignKey(
        #親の投稿があれば関連付ける
        #models.ForeignKeyの第一引数は必ずモデル名．今回は自身なので'self'
        'self',
        related_name='replies', #リレーション名．使用時はreplies.parent(repliesのparent)という形であるため
        on_delete=models.CASCADE, #親投稿が削除されたら自動で削除される
        null=True,blank=True #null:databaseレベルの空,blank:フォームや管理画面レベルの空
        )
    author=models.ForeignKey(
        User, #一人のユーザが複数のpostを持つため，ForeignKeyを使用． #TODO:マイページにてuser.author.all()でユーザの投稿一覧を作成．
        related_name='posts',
        on_delete=models.CASCADE,
        null=True,blank=True
    )
    
    def __str__(self):
        return self.content if self.content else "No content(polls/models_test.py)"
    
    def update_like_count(self,number):
        if self.like_count+number>=0:
            self.like_count+=number
            self.save()
            return True
        else:
            return False
            
    class Meta:
        ordering=['-post_date'] #postを投稿順に並び替え

