from  django.urls import path
from . import views




urlpatterns = [

    path('login/', views.login_view, name='login_view'),
    path('register_view', views.register_view, name='register_view'),
    path('logout_view', views.logout_view, name='logout_view'),
    path('listuser_view', views.listuser_view, name='listuser_view'),
    path('dashboard_admin', views.dashboard_admin, name='dashboard_admin'),
    path('dashboard_presi', views.dashboard_presi, name='dashboard_presi'),
    path('dashboard_treso', views.dashboard_treso, name='dashboard_treso'),
    path('dashboard_secret', views.dashboard_secret, name='dashboard_secret'),
]