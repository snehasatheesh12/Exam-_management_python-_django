from django.urls import path
from common import views

urlpatterns = [
    path('institute/create/', views.institute_create, name='institute_create'),
    path('institute_list/', views.institute_list, name='institute_list'),
    path('institutes/approve/<int:institute_id>/', views.approve_institute, name='institute_approve'),
    path('institutes/reject/<int:institute_id>/', views.reject_institute, name='institute_reject'),
       
]
