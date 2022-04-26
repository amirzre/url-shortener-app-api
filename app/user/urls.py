from django.urls import path

from user import views


app_name = 'user'

urlpatterns = [
    path('list/', views.ListProfilesUserView.as_view(), name='list'),
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('login/',
         views.CustomTokenObtainPairView.as_view(),
         name='UserSerializerWithToken'
         ),
    path('profile/<int:pk>/', views.ProfileUserView.as_view(), name='profile'),
]
