from django.urls import path, include

from users.views import SignUp

urlpatterns = [
    path('', include('django.contrib.auth.urls')),

    path('register/', SignUp.as_view(), name='register'),
]
