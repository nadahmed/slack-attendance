"""slack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from django.urls.conf import include

admin.site.site_header = 'Hivecore Attendance Administration'                    # default: "Django Administration"
# admin.site.index_title = 'Timesheet'                # default: "Site administration"
# admin.site.site_title = 'HTML title from adminsitration' # default: "Django site admin"

urlpatterns = [
    path('attendance/', include('attendance.urls')),
    path('admin/', admin.site.urls),
]