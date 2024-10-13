from django.urls import path

from Admin import views




app_name = 'Admin'

urlpatterns = [
        path('admin_home/', views.admin_home, name='admin_home'),
        path('view_registered_User/', views.view_registered_User, name='view_registered_User'),
        path('handle_user_registration/<int:user_id>/<str:action>/', views.handle_user_registration, name='handle_user_registration'),
        path('complaint-list/', views.complaint_list_admin, name='complaint_list_admin'),
        path('admin/respond-complaint/<int:complaint_id>/', views.respond_to_complaint, name='respond_to_complaint'),
        ]