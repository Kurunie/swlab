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
    path('q/<str:type>/<int:id>/', q_views.singleq, name='q'),
    path('search/', q_views.search, name='search'),
    path('login/', q_views.mylogin, name='login'),
    path('logout/', q_views.mylogout, name='logout'),
    path('user/', q_views.userpage, name='user'),
    path("exam/<int:sid>/<int:pid>/", q_views.exam, name='exam'),
    path("a_exam/<int:sid>/<int:pid>/", q_views.a_exam, name='a_exam'),
    path("calGrade/", q_views.calGrade),
    path("a_calGrade/", q_views.a_calGrade),
    path("answer/<int:id>/", q_views.lookAnswer, name="answer"),
    path("a_answer/<int:id>/", q_views.a_lookAnswer, name="a_answer"),
    path("rewind/<int:id>/", q_views.rewind, name="rewind"),
    path("sub_rewind/", q_views.sub_rewind, name="sr"),
    path("user/export/", q_views.export_excel, name="export"),
    path("d/<str:type>/<int:id>/<int:did>/", q_views.discussion, name="ds"),
    path("add_dis/", q_views.add_dis, name="add_d"),
    path("add_rep/", q_views.add_rep, name="add_r"),
    path("my_dis/<str:type>/<int:id>", q_views.my_dis, name="my_dis"),
    path("change_s/", q_views.change_s, name="change_s"),
    path("add_autop/", q_views.add_auto_paper, name="add_ap"),
    path("del_ap/<int:id>/", q_views.del_apaper, name="del_ap"),
    path("del_ag/<int:id>/", q_views.del_agrade, name="del_ag"),
]
