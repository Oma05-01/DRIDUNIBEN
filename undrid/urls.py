from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),

    path('faculties/', views.faculty_list_view, name='faculty_list'),
    path('faculties/<str:code>/', views.faculty_detail_view, name='faculty_detail'),

    path('departments/', views.department_list_view, name='department_list'),
    path('departments/<str:code>/', views.department_detail_view, name='department_detail'),

    path('articles/', views.article_list, name='article_list'),
    path('create-article', views.create_article, name='create_article'),
    path('article/<str:pk>/', views.article_detail, name='article_detail'),

    path('contributors/search/', views.search_contributors, name='search_contributors'),
    path('contributors/add/', views.add_contributor, name='add_contributor'),
    path('contributors/', views.contributor_list, name='contributor_list'),
    path('contributors/<str:pk>/', views.view_contributor, name='view_contributor'),
    path('contributor/<str:pk>/articles/', views.articles_by_researcher, name='articles_by_researcher'),

    path('articles/<str:pk>/edit/', views.edit_article, name='edit_article'),
    path('articles/<str:pk>/delete/', views.delete_article, name='delete_article'),
    path('articles/<str:pk>/toggle-publish/', views.toggle_publish, name='toggle_publish')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)