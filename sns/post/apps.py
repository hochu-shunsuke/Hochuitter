from django.apps import AppConfig


class PostConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'post'
    
    def ready(self):
        print("postアプリが起動しました!(post/apps.pyにて表示中)")
    #Appconfigクラスにready()メソッドを用いるとアプリ起動時に実行される．