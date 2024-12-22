from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE) #各Userに対しProfileは一つしかないことの明示，Userが削除されたら自動で消える(on_deleteの部分)
    date_joined=models.DateTimeField(auto_now_add=True) #サービスに登録した日時
    bio=models.TextField(max_length=400) #biography(ユーザの自己紹介やプロフィールの説明文)
    icon_picture=models.ImageField(upload_to='profile_pics/', blank=True, null=True) #ImageFieldではdjangoがファイルを扱うためのAPIを提供してくれる．#TODO:Django documentation
    
    
    def __str__(self):
        return self.user.username #Userのusernameを参照している．Profile.userの定義部分でUserをOneToOneで見ているからそのまま引き継いでいる
    
class Follow(models.Model):
    follower=models.ForeignKey(User,on_delete=models.CASCADE,related_name='following') #フォロワー
    followed=models.ForeignKey(User,on_delete=models.CASCADE,related_name='followed') #フォロー中
    
    
    class Meta:
        unique_together=('follower','followed') #unique_togetherは一位制約性をデータベースレベルで担保するから，同一ユーザの重複フォローを防げる!!!!
        