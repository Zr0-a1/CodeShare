
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('snippet/<int:pk>/', views.detail, name='detail'),
    path('upload/', views.upload_code, name='upload'),
    path('download/<int:pk>/', views.download_code, name='download'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('comment/<int:pk>/', views.add_comment, name='add_comment'),
    path('report/<int:pk>/', views.report_snippet, name='report_snippet'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('notifications/', views.user_notifications, name='notifications'),
]
