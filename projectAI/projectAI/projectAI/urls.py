from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from appAI.urls import *

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', include('appAI.urls')),
    

]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)