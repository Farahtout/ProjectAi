from django.urls import path
from . import views
urlpatterns =[
    path('',views.home, name='home'),
    path('projectList/', views.projectList, name='projectList'),
    path('employeeList/', views.employeeList, name='employeeList'),
    path('addproject/', views.addproject, name='addproject'),
    path('addemployee/', views.addemployee, name='addemployee'),
    path('projectview/<int:project_id>/', views.projectview, name='projectview'),
    path('employeeview/<int:employee_id>/', views.employeeview, name='employeeview'),
    path('taskview/<int:task_id>/', views.taskview, name='taskview'),
    path('delete_project/<int:project_id>/', views.delete_project, name='delete_project'),
    path('completed/<int:project_id>/', views.completed, name='completed'),
    path('panding/<int:project_id>/', views.panding, name='panding'),
    path('canceled/<int:project_id>/', views.canceled, name='canceled'),
    path('add_employee/<int:project_id>/', views.add_employee, name='add_employee'),
    path('add_employeetask/<int:task_id>/', views.add_employeetask, name='add_employeetask'),
    path('react/',views.react,name='react'),
    path('api/employees/', views.get_employee_data, name='get_employee_data'),
    path('delete_task/<int:taskId>/', views.delete_task, name='delete_task'),
    path('create_task/<int:project_id>/', views.create_task, name='create_task'),
    path('api/projects/', views.get_project_data, name='get_project_data'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('register/',views.RegisterView.as_view(),name='register'),
    path('logout/',views.logout_view,name="logout"),




]