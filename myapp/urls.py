from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/<str:user_name>/', views.profile, name='profile'),
    path('profile_admin/<str:user_name>/', views.profile_admin, name='profile_admin'),
    path('profile_hr/<str:user_name>/', views.profile_hr, name='profile_hr'),
    path('profile_data/<str:user_name>/', views.profile_data, name='profile_data'),
    path('profile_data_hr/<str:user_name>/', views.profile_data_hr, name='profile_data_hr'),
    path('profile_data_admin/<str:user_name>/', views.profile_data_admin, name='profile_data_admin'),
    path('hobbies/<str:user_name>/', views.hobbies, name='hobbies'),
    path('hobbies_admin/<str:user_name>/', views.hobbies_admin, name='hobbies_admin'),
    path('hobbies_hr/<str:user_name>/', views.hobbies_hr, name='hobbies_hr'),
    path('home_skills/<str:user_name>/', views.home_skills, name='home_skills'),
    path('home_skills_admin/<str:user_name>/', views.home_skills_admin, name='home_skills_admin'),
    path('home_skills_hr/<str:user_name>/', views.home_skills_hr, name='home_skills_hr'),
    path('character/<str:user_name>/', views.character, name='character'),
    path('character_admin/<str:user_name>/', views.character_admin, name='character_admin'),
    path('character_hr/<str:user_name>/', views.character_hr, name='character_hr'),
    path('find_partner/<str:user_name>/', views.find_partner, name='find_partner'),
    path('find_partner_admin/<str:user_name>/', views.find_partner_admin, name='find_partner_admin'),
    path('find_partner_hr/<str:user_name>/', views.find_partner_hr, name='find_partner_hr'),
    path('add_user_admin/<str:user_name>/', views.add_user_admin, name='add_user_admin'),
    path('delete_user/<str:user_name>/', views.delete_user, name='delete_user'),
    path('edit_user_data/<str:user_name>/', views.edit_user_data, name='edit_user_data'),
    path('view_profilies_hr/<str:user_name>/', views.view_profilies_hr, name='view_profilies_hr'),
    path('view_profilies_admin/<str:user_name>/', views.view_profilies_admin, name='view_profilies_admin'),
]