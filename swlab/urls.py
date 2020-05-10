"""swlab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from question_manage import views as q_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', q_views.index, name="qlist"),
    path('q/<int:id>/', q_views.singleq, name='q'),
    path('search/', q_views.search, name='search'),
    path('login/', q_views.mylogin, name='login'),
    path('logout/', q_views.mylogout, name='logout'),
    path('user/', q_views.userpage, name='user'),
    path("exam/<int:sid>/<int:pid>/", q_views.exam, name='exam'),
    path("calGrade/", q_views.calGrade),
    path("answer/<int:id>/", q_views.lookAnswer, name="answer"),
    path("rewind/<int:id>/", q_views.rewind, name="rewind"),
    path("sub_rewind/", q_views.sub_rewind, name="sr"),
    path("user/export/", q_views.export_excel, name="export"),
]
