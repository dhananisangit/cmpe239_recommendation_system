from django.conf.urls import url

from HR_recommendation_system import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home$', views.home, name='home'),
    url(r'v1/login$', views.login),

]
