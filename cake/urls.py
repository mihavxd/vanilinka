from django.urls import path
from .views import *
from .sitemap import StaticViewsSitemap, DynamicViewsSitemap
from django.contrib.sitemaps.views import sitemap



sitemaps = {
    'static': StaticViewsSitemap,
    'dynamic': DynamicViewsSitemap
}

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('category/<str:slug>/', PostsByCategory.as_view(), name='category'),
    path('tag/<str:slug>/', PostsByTag.as_view(), name='tag'),
    path('post/<str:slug>/', GetPost.as_view(), name='post'),
    path('search/', Search.as_view(), name='search'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path('dostavka/', AboutDostavka.as_view(), name='dostavka'),
    path('contactforms/', ContactForms, name='contactforms'),
]