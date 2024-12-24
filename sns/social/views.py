from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from post.models import Post #postアプリのmodelsからPostをimport
#from django.contrib.auth.decorators import login_required


def userpage(request,user_id): #requestにはurls.py見るとuser_idが入ってる
    #Userクラスのidでuserを代入，もしpkがデータベースに存在しなかったら404を返す
    user=get_object_or_404(User, pk=user_id)
    user_posts=Post.objects.filter(user=user)
    return render(request,'social/userpage.html',{
        'username':user.username,
        'user_posts':user_posts,
        'user_id':user.id
})
#@login_requredを用いて,userpageが呼び出されたときに閲覧するユーザページのユーザidとログイン中のidが等しい時のみにユーザページにここはあなたのサイトです！とか表示できるし，そこからプロフ編集をできる
