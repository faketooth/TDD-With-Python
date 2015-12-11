"""superlists URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))

Changes from Django1.7:
    http://stackoverflow.com/questions/34096424/django-support-for-string-view-arguments-to-url-is-deprecated-and-will-be-rem
"""
from django.conf.urls import url
from django.contrib import admin
from lists import views

# Holy Mother Fuck. Commented this ''. It's completely different in django1.9
urlpatterns = [
    #'',
    url(r'^$', views.home_page),
]
