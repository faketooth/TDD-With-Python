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
	http://redsymbol.net/articles/django-attributeerror-str-object-no-attribute-resolve/
	http://stackoverflow.com/questions/7020523/str-object-has-no-attribute-resolve-when-access-admin-site
"""
from django.conf.urls import url
from django.contrib import admin
from lists import views

# Holy Mother of God. Commented this ''. It's completely different in django1.9
# urlpatterns should be a Python list of url() instances. yes. '' is not instance of url()
urlpatterns = [
    #'',
    url(r'^$', views.home_page),
	url(r'^lists/the-only-list-in-the-world/$', views.view_list),
	url(r'^lists/new$', views.new_list),
]
