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
    follower=models.ForeignKey(User,on_delete=models.CASCADE,related_name='followers') #フォロワー follow.followers.all()のように使用
    followed=models.ForeignKey(User,on_delete=models.CASCADE,related_name='following') #フォロー中 follow.following.all（）のように使用
    ff_date=models.DateTimeField(null=True,blank=True) #相互フォローが完了した日(check_ff_is_activeにて初期値を設定)
    ff_is_active=models.BooleanField(default=False)

    
    def check_ff_is_active(self):
        #自身がフォローしているユーザが自身をフォローしているか判定
        if self.follower!=self.followed and Follow.objects.filter(follower=self.followed,followed=self.follower).exists():
            self.ff_is_active=True
            if not self.ff_date:
                self.ff_date=models.DateTimeField(auto_now_add=True) #相互フォロー状態になったときにff_date(相互フォローが完了した日)を追加
        else:
            #相互フォローが解除されても，再フォロー時にデータベースの重複を防ぐためff_dateを消さずに一時的にff_is_activeをFalseにする
            self.ff_is_active=False
        return self.ff_is_active
    
    
    def save(self, *args, **kwargs):
        # モデルが保存される前に相互フォローの状態をチェック
        self.check_ff_is_active()
        super().save(*args, **kwargs)
    #save関数はgrokAIにより作成しました．
    """
    save()はdjango標準の機能であるが,今回はcheck_ff_is_activeをオーバーライド(上書き)する必要があるため修正を加えている．
    saveの引数*args,*kwagrsはそれぞれpythonの標準引数!
    *args(アーグス):任意の数の位置引数を意味する．関数にどれだけの要素が渡されてもそれらを一つのタプルとして扱うことが可能!!!
        (例)def function(*args):;print(*args);function(1,2,3)=(1,2,3);function(1,2,3,4,5)=(1,2,3,4,5)
    **kwargs(ケーワグス):任意の数のキーワード引数．引数を辞書のように扱う!!!
        (例)def def test_function(**kwargs):;print(kwargs)  #kwargsは辞書になる
            test_function(name="Alice",age=30)={'name':'Alice','age':30}
    
    関数のスケーラビリティを高めるためにpythonで標準的に使用される!!!!!!!!!
    """
    
    
    class Meta:
        unique_together=('follower','followed') #unique_togetherは一位制約性をデータベースレベルで担保するから，同一ユーザの重複フォローを防げる!!!!
        