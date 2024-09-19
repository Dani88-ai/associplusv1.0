from  django.urls import path
from . import views




urlpatterns = [

    path('adherent_view', views.adherent_view, name='adherent_view'),
    path('adherent_add', views.adherent_add, name='adherent_add'),
    path('adherent/edit/<int:adherent_id>/', views.adherent_edit, name='adherent_edit'),
    path('adherents/delete/<int:adherent_id>/', views.adherent_delete, name='adherent_delete')
]