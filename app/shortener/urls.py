from django.urls import path

from shortener import views


app_name = 'shortener'

urlpatterns = [
    path('', views.ShortUrlList.as_view(), name='list'),
    path('create/', views.ShortenUrl.as_view(), name='create'),
    path('<str:short_id>/',
         views.GetOrginalUrl.as_view(),
         name='original_link'
         ),
    path('shorturl/<int:pk>/',
         views.RetrieveShortUrl.as_view(),
         name='shorturl'
         ),
]
