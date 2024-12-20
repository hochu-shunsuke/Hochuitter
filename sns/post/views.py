from django.shortcuts import render

#url.pyでurl作成したあとで，views.pyに該当の関数を作成しreturn renderでhtmlなり関数の戻り値なりを返すかな

def index(request):
    return render(request,'post/index.html')

