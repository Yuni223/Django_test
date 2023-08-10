"""
URL configuration for Django_test project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
# conf : django 프로젝트의 기본 폴더, 우리는 Django_test임

urlpatterns = [
    path('board/', include('board.urls')),
    path('blog/', include('blog.urls')),
    path('admin/', admin.site.urls),
    path('markdownx/', include('markdownx.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('single_pages.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
# +=을 하는 이유는 사진을 여러장 들고올 때 때문에 누적시키기 위해서

