from django.urls import path

from User import views




app_name = 'User'

urlpatterns = [
        path('index/', views.index, name='index'),
        path('register/', views.register, name='register'),
        path('login/', views.login, name='login'),
        path('user_home/', views.user_home, name='user_home'),
        path('profile/', views.user_profile, name='user_profile'),
        path('add-deposit/', views.deposit, name='deposit'),
        path('add-transfer/',views.transfer, name='transfer'),
        path('get-user-details/',views.get_user_details, name='get_user_details'),
        path('transaction-details/', views.transaction_details, name='transaction_details'),
        path('register_complaint/', views.register_complaint, name='register_complaint'),
        path('complaint-list/', views.complaint_list, name='complaint_list'),
        path('update_password/', views.update_password, name='update_password'),
        
        ]