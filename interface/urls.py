from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('possibleprivilege/add', views.add_possible_priv, name="add_possible_priv"),
    path('possibleprivilege/delete', views.delete_possible_priv, name="delete_possible_priv"),
    path('role/add', views.add_role, name="add_role"),
    path('role/delete', views.delete_role, name="delete_role"),
    path('assign', views.assign_priv_to_role, name="assign_priv_to_role"),
    path('remove', views.remove_priv_from_role, name="remove_priv_from_role")
]