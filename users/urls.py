from django.urls import path

from users.views import Users


app_name = 'users'

urlpatterns = [
    path('', Users.as_view())
]
