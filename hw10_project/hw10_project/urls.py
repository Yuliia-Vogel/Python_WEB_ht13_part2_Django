from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  
    path('users/', include(('users.urls', 'users'), namespace='users')),  # Додано простір імен 'users'
    path("quotes/", include("quotes.urls")),
    # path('users/', include('users.urls')),
]
