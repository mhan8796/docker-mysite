from django.urls import path

from . import views


app_name = 'info'
urlpatterns = [
    path('', views.index, name='index'),
    path('confluence-admin/', views.get_confluence_space_admin, name='confluence-admin'),
    path('bitbucket-admin/', views.get_bb_project_admin, name='bitbucket-admin'),
    path('jira-admin/', views.get_jr_project_admin, name='jira-admin'),
]