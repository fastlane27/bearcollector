from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('bears/', views.bears_index, name='bears_index'),
    path('bears/<int:bear_id>/', views.bears_detail, name='bears_detail'),
    path('bears/create/', views.BearCreate.as_view(), name='bears_create'),
    path('bears/<int:pk>/update/', views.BearUpdate.as_view(), name='bears_update'),
    path('bears/<int:pk>/delete/', views.BearDelete.as_view(), name='bears_delete'),
]
