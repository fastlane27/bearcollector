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
    path('bears/<int:bear_id>/add_feeding/', views.add_feeding, name='add_feeding'),
    path('bears/<int:bear_id>/delete_feeding/<int:feeding_id>/', views.delete_feeding, name='delete_feeding'),
    path('bears/<int:bear_id>/assoc_toy/<int:toy_id>/', views.assoc_toy, name='assoc_toy'),
    path('bears/<int:bear_id>/unassoc_toy/<int:toy_id>/', views.unassoc_toy, name='unassoc_toy'),
    path('toys/', views.ToyList.as_view(), name='toys_index'),
    path('toys/<int:pk>/', views.ToyDetail.as_view(), name='toys_detail'),
    path('toys/create/', views.ToyCreate.as_view(), name='toys_create'),
    path('toys/<int:pk>/update/', views.ToyUpdate.as_view(), name='toys_update'),
    path('toys/<int:pk>/delete/', views.ToyDelete.as_view(), name='toys_delete'),
]
