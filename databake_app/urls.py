from django.urls import path
from . import views


urlpatterns = [
    path('', views.form),
    path('registered', views.registered),
    path('logout', views.logout),
    path('login', views.login),
    path('homepage', views.homepage),
    path('profile', views.profile),
    path('my_recipes', views.my_recipes),
    path('categories', views.categories),
    path('recipe/<int:recipe_id>', views.recipe_info),
    path('create', views.create_recipe),
    path('edit_profile', views.edit_profile),
    path('add_recipe', views.add_recipe),
    # path('metric', views.metric),
    # path('imperial', views.imperial),
    # path('percent', views.percent),
    # path('add_ingredient', views.add_ingredient),
    path('update_profile', views.update_profile),
    path('recipe/<int:recipe_id>/delete', views.delete_recipe),
    path('recipe/<int:recipe_id>/update', views.update),
    path('recipe/<int:recipe_id>/add', views.add_recipe),
    path('recipe/<int:recipe_id>/remove', views.remove_recipe),

    
    path('recipe/<int:recipe_id>/edit', views.edit_recipe),
    
]