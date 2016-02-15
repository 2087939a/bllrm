from django.conf.urls import patterns, include, url
from django.contrib import admin
from app import views
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),

)