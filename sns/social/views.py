from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from post.models import Post #postアプリのmodelsからPostをimport

def userpage(request,user_id): #requestにはurls.py見るとuser_idが入ってる
    #Userクラスのidでuserを代入，もしpkがデータベースに存在しなかったら404を返す
    user=get_object_or_404(User, pk=user_id)
    user_posts=Post.objects.filter(user=user)
    return render(request,'social/userpage.html',{'username':user.username,'user_posts':user_posts})
