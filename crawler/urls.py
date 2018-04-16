from django.conf.urls import url
from . import views

app_name = 'crawler'
urlpatterns = [
    url(r'^crawler/$',views.crawler,name='crawler'),
]