"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from DjangoUeditor import urls as DjangoUeditor_urls
urlpatterns = [
    url(r'^himg$', 'himg.views.index', name='hindex'),
    url(r'^himg/login$', 'himg.views.login_view', name='hlogin'),
    url(r'^himg/logout$', 'himg.views.logout_view', name='hlogout'),
    url(r'^himg/regist$', 'himg.views.regist', name='hregist'),
    url(r'^himg/column/(?P<column_slug>[^/]+)/$', 'himg.views.column_detail', name='hcolumn'),
    url(r'^himg/himg/(?P<pk>\d+)/(?P<article_slug>[^/]+)/$', 'himg.views.article_detail', name='harticle'),
    url(r'^himg/declaration$', 'himg.views.declaration', name='hdeclaration'),
    url(r'^himg/aboutus$', 'himg.views.aboutus', name='haboutus'),
    #---------------------------------------------------------------------
    url(r'^news$', 'news.views.news_page', name='news_page'),

    url(r'^login$', 'news.views.login_view', name='login'),
    url(r'^logout$', 'news.views.logout_view', name='logout'),
    url(r'^regist$', 'news.views.regist', name='regist'),

    url(r'^column/(?P<column_slug>[^/]+)/$', 'news.views.column_detail', name='column'),
    url(r'^news/(?P<pk>\d+)/(?P<article_slug>[^/]+)/$', 'news.views.article_detail', name='article'),
    url(r'^info$', 'news.views.cusInfo', name='cusInfo'),
    url(r'^declaration$', 'news.views.declaration', name='declaration'),
    url(r'^aboutus$', 'news.views.aboutus', name='aboutus'),
    #---------------------------------------------------------------------
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'news.views.index', name='index'),
    url(r'^cloud9$', 'news.views.cloud9', name='cloud9'),
    url(r'^pyspider$', 'news.views.pyspider', name='pyspider'),
    url(r'^contact$', 'news.views.contact', name='contact'),

]
# use Django server /media/ files
from django.conf import settings

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)