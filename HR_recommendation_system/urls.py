from django.conf.urls import url

from HR_recommendation_system import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
