from django.urls import path, include
from .views import *

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('test', test),
    path('login', login),
    path('admin', sys_home),
    path('exit', exit),
]
