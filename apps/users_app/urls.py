
from django.conf.urls import url
from . import views
urlpatterns = [

    url(r'^$', views.index),
    url(r'^clear$',views.clear),
    url(r'^create$',views.add),
    url(r'^join/(?P<item_id>\d+)$',views.join),
    url(r'^create_item$',views.create),
    url(r'^(?P<item_id>\d+)$',views.about_item),
    url(r'^delete/(?P<item_id>\d+)$',views.delete),
    url(r'^delete/list/(?P<item_id>\d+)$',views.delete_from_list),
    ]



