from django.contrib import admin
from django.urls import path, include  # <--- importar include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('config.urls')),  # <--- agregar coma
]
