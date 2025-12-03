from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Browse + Detail
    path('browse/', views.browse, name='browse'),
    path('snippet/<int:pk>/', views.detail, name='detail'),
    path('snippet/<int:pk>/report/', views.report_snippet, name='report_snippet'),  # ✅ added
    path('snippet/<int:pk>/delete/', views.delete_snippet, name='delete_snippet'),

    # Upload/Download
    path('upload/', views.upload_code, name='upload'),
    path('download/<int:pk>/', views.download_code, name='download'),

    # Auth
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Profile + Dashboard
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/dashboard/', views.user_dashboard, name='user_dashboard'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change-password/', views.change_password_dashboard, name='change_password'),
    path('profile/delete/', views.delete_account, name='delete_account'),

    # Notifications
    path('notifications/', views.user_notifications, name='notifications'),
    path('notifications/mark-all-read/', views.mark_all_read, name='mark_all_read'),
]
