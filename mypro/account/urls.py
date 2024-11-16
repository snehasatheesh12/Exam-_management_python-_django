
from django.urls import path
from account import views

urlpatterns = [
    path('',views.home,name='home'),
    path('admin_signup_view', views.admin_signup_view,name='admin_signup_view'),
    path('admin_login_view', views.admin_login_view,name='admin_login_view'),
    path('is_admin', views.is_admin,name='is_admin'),
    path('afterlogin_view', views.afterlogin_view,name='afterlogin_view'),
    path('admin_dashboard', views.admin_dashboard,name='admin_dashboard'),
    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(),name='activate'),
    path('handel_logout',views.handel_logout,name='handel_logout'),
    path('principleRegistration',views.principleRegistration,name='principleRegistration'),
    path('principleLogin',views.principleLogin,name='principleLogin')


    
    
]
