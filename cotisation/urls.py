from  django.urls import path
from . import views




urlpatterns = [
    
    path('cotisation/', views.cotisation_view, name='cotisation_view'),
    path('cotisation_add', views.cotisation_add, name='cotisation_add'),
    path('cotisation/edit/<int:cotisation_id>/', views.cotisation_edit, name='cotisation_edit'),
    path('cotisation/details/<int:cotisation_id>/', views.cotisation_details, name='cotisation_details'),
    path('cotisation/delete/<int:cotisation_id>/', views.cotisation_delete, name='cotisation_delete')
]