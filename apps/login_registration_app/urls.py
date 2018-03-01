
from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'clear$',views.clear),
    url(r'registration_validator$', views.registration_validator),
    url(r'login_validator$', views.login_validator),
    ]

