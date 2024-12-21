from django.db import models

class Post(models.Model):
    content=models.CharField(max_length=280)
    like_count=models.PositiveIntegerField(default=0)
    post_date=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.content
    
    def update_like_count(self,number):
        if self.like_count+number>=0:
            self.like_count+=number
            self.save()
        else:
            raise ValueError("いいね数は負の値に設定できません")
        #いいねの追加，取り消しに対応
    
    class Meta:
        ordering=['-post_date']
        #postを投稿順で並び替え

class Comment(models.Model):
    post=models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE,null=True,blank=True)#親オブジェクトpostに対するcomment
    reply=models.ForeignKey('self',related_name='replies',on_delete=models.CASCADE,null=True,blank=True)#親オブジェクトcommentに対するcomment
    #null:データベースレベルでの空,blank:フォームや管理画面レベルでの空
    """
    ForeignKey(Post):多対一の関係を示す(1つのpostに対して多数のcommentを関連づける)
    related_name='comment':逆方向の関係に名前をつけるためのオプション
    on_delete=models.CASCADE:親オブジェクト(Post)を削除すると関連オブジェクトを削除
    """
    comment=models.CharField(max_length=280)
    like_count=models.PositiveIntegerField(default=0)
    post_date=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.comment
    
    def update_like_count(self,number):
        if self.like_count+number>=0:
            self.like_count+=number
            self.save()
        else:
            raise ValueError("いいね数は負の値に設定できません")
        #いいねの追加，取り消しに対応

    class Meta:
        ordering=['-like_count','-post_date']
        #commentをいいね数順に並び替え



"""
models.PROTECT: 削除を禁止してエラーを発生させる。
models.SET_NULL: 子オブジェクトのフィールドをNULLに設定（null=Trueが必要）。
models.SET_DEFAULT: 子オブジェクトのフィールドをデフォルト値に設定。
3. データベースに保存される仕組み
ForeignKeyフィールドを定義すると、データベースのCommentテーブルにpost_idというカラムが追加されます。

post_idは、Postテーブルの主キー（デフォルトではid）を参照します。
Commentモデルの各インスタンスは、post_idを持つことでどのPostに属するかを記録します。
例:

Comment ID	comment	            post_id
1	        いい投稿ですね!        1
2	        もっと教えてほしいです  1
3	        素晴らしいですね！	    2
4. 利用例
4.1 コメントを作成する
python
コードをコピーする
# 1つの投稿を取得
post = Post.objects.get(id=1)

# コメントを作成
comment = Comment.objects.create(post=post, comment="素晴らしい投稿ですね！")
4.2 投稿に紐づいたコメントを取得する
python
コードをコピーする
# 投稿に紐づくコメントを取得
comments = post.comments.all()
for c in comments:
    print(c.comment)
4.3 投稿が削除された場合
python
コードをコピーする
# 投稿を削除
post.delete()

# その投稿に関連付けられたコメントも自動で削除される（CASCADEの効果）
5. 結論
post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)は、以下のことを実現します：

コメントがどの投稿に属しているかを記録（post_id）。
投稿から関連するコメントを簡単に取得（post.comments.all()）。
投稿が削除されたら関連コメントも削除（CASCADE）。
"""