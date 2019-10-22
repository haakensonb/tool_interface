from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('possibleprivilege/add/<priv>', views.add_possible_priv, name="add_possible_priv"),
    path('possibleprivilege/delete/<priv>', views.delete_possible_priv, name="delete_possible_priv")
]