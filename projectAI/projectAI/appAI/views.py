from django.shortcuts import render
from django.core.mail import EmailMessage
import random
import string
from datetime import date
from decimal import Decimal
from django.utils import timezone

from .models import *
from datetime import datetime
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .serializers import EmployeeSerializer,project_generalSerializer,LoginSerializer
from django.contrib.auth.models import User, Group
from django.contrib import auth
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import logout


from rest_framework import status




# Create your views here.
def home(request):
    print(request.user)
    return render(request,'home.html')





def projectList(request):
    user=request.user
    projects=project_general.objects.all()
    
    todayprojects = project_general.objects.filter(endDate=date.today())
    projectslate = project_general.objects.filter(endDate__lt=timezone.now().date())
    print(projectslate)
    for project in projectslate:
       
        if project.status !='completed':
            print(project)
            project.status='cancelled'
            project.save()
  
    if user.is_staff:
        projects=project_general.objects.all()
    else:
        emp=employee.objects.get(username=user)
        projects=emp.Get_All_Projects() 
    
    return render(request,'projectList.html',{'projects':projects,'todayprojects':todayprojects})

def employeeList(request):
    employees = None

    if request.user.is_staff:
        employees=employee.objects.all()
   
    return render(request,'employeeList.html',{'employees':employees})
 

def addproject(request):
    allemp=employee.objects.all()
    type='other'
    if request.method=='POST':
        selected_index = request.POST.get('type')
        if selected_index==0:
            type='ai'
        else:
            type='other'
        name=request.POST['name']
        description=request.POST['description']
        startDate=request.POST['startDate']
        endDate=request.POST['endDate']
        cost=request.POST['cost']
        new_project=project_general.objects.create(
             name=name,
            description=description,
            startDate=startDate,
            endDate=endDate,
            type=type,
            cost=Decimal(cost)
,

        )
        new_project.clean()
        new_project.save()
        return redirect('projectList')
    return render(request,'addproject.html',{'allemp':allemp})

def generate_username(first_name, last_name):
    random_number = random.randint(100, 999)
    username = f"{first_name.lower()}{last_name.lower()}{random_number}"
    return username

def generate_password(length=10):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

def addemployee(request):
    if request.user.is_staff:
        position='ai'
        gender='M'
        if request.method=='POST':
            email = request.POST['email']
            FirstName=request.POST['FirstName']
            LastName=request.POST['LastName']
            address=request.POST['address']
            email=request.POST['email']
            birthday=request.POST['birthday']
            selected_index = request.POST.get('position')
            if selected_index==0:
                position='ai'
            else:
                position='software'
            selected_index = request.POST.get('gender')
            if selected_index==0:
                gender='M'
            else:
                gender='F' 
            certification=request.POST['certification']
            username=generate_username(FirstName, LastName)
            password=generate_password(5)
            userpass=password
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_staff=False
            user.is_superuser=False  
            user.is_active = True
            user.save()
            emp_group = Group.objects.get(name='ai and software')
            emp_group.user_set.add(user)
            
            new_employee=employee.objects.create(
                username=user,
                FirstName=FirstName,
                LastName=LastName,
                email=email,
                address=address,
                position=position,
                birthday=birthday,
                gender=gender,
                certification=certification
            )
            new_employee.save()
            
            mail_subject = 'dear, '+FirstName+" "+LastName+'. you can log in to ProjectAI using this account'
            message = 'username: '+user.username+'--'+'password:'+userpass
            send_to=[user.email]
            email=EmailMessage(mail_subject, message, 'farahhtout15@example.com', send_to)
            email.send() 
            return redirect('employeeList')
        return render(request,'addemployee.html')

def projectview(request,project_id):
    id=project_id
    project=project_general.objects.get(pk=id)
    employees = project.employees.all()  
    allemp=employee.objects.all()
    if request.method=='POST':
        project.name=request.POST['name']
        project.description=request.POST['description']
        project.startDate=request.POST['startDate']
        project.endDate=request.POST['endDate']
        project.save()
        return redirect('projectList')
    tasks=project.Get_All_Project_Tasks()
    return render(request,'projectview.html',{'project':project,'tasks':tasks,'employees':employees,'allemp':allemp})

def employeeview(request,employee_id):
    if request.user.is_staff:
        id=employee_id
        employeeid=employee.objects.get(pk=id)
        if request.method=='POST':
            employeeid.FirstName=request.POST['FirstName']
            employeeid.LastName=request.POST['LastName']
            employeeid.address=request.POST['address']
            employeeid.email=request.POST['email']
            employeeid.certification=request.POST['certification']
            employeeid.save()
            return redirect('employeeList')
        projects=employeeid.Get_All_Projects()
        tasks=employeeid.Get_All_tasks()
   
               
    
    return render(request,'employeeview.html',{'employeeid':employeeid,'projects':projects,'tasks':tasks})
        

def taskview(request,task_id):
    id=task_id
    task=project_task.objects.get(pk=id)
    taskemployee=task.employee_id
    print(taskemployee)
    projectid=project_general.objects.get(name=task.project_id)
    employees = projectid.employees.all() 
    if request.method=='POST':
        task.name=request.POST['name']
        task.description=request.POST['description']
        task.startDate=request.POST['startDate']
        task.endDate=request.POST['endDate']
        task.save()
        return redirect('projectview', project_id= projectid.id)
    
    return render(request,'taskview.html',{'task':task,'employees':employees,'taskemployee':taskemployee,'projectid':projectid})


def delete_project(request,project_id):
    id=project_id
    if request.method == 'DELETE':
        project=project_general.objects.get(pk=id)
        project.delete()
    return redirect('projectList')

def completed(request,project_id):
    print(project_id)
    id=project_id
    project=project_general.objects.get(pk=id)
    print(project.name)
    print(project.status)
  
    project.status='completed'
    project.save()
    print(project.status)
    return redirect('projectList')

def panding(request,project_id):
    id=project_id
    print(project_id)
    project=project_general.objects.get(pk=id)
    project.status='panding'
    project.save()
    return redirect('projectList')

def canceled(request,project_id):
    id=project_id
    project=project_general.objects.get(pk=id)
    project.status='cancelled'
    project.save()
    return redirect('projectList')

def add_employee(request,project_id):
    id=project_id
    project=project_general.objects.get(pk=id)
    selected_indices = request.GET.getlist('indices')
    print(selected_indices)
    for index in selected_indices:
        selectedemployee=employee.objects.get(pk=index)
        project.employees.add(selectedemployee)
        project.save()
    return redirect('projectList')


def add_employeetask(request,task_id):
    task=project_task.objects.get(pk=task_id)
    selected_indices = request.GET.getlist('indices')
    for index in selected_indices:
        selectedemployee=employee.objects.get(pk=index)
        task.employee_id=selectedemployee
        task.save()
    return redirect('taskview',task_id=task_id)
   


def delete_task(request,taskId):
    id=taskId
    if request.method == 'DELETE':
        task=project_task.objects.get(pk=id)
        task.delete()
    return redirect('projectList')


def create_task(request,project_id):
    print("start")
    project=project_general.objects.get(pk=project_id)
    employees = project.employees.all()  
    if request.method=='POST':
        print('s')
        name=request.POST['name']
        startDate=request.POST['startDate']
        endDate=request.POST['endDate']
        description=request.POST['description']
        project_id=project_id
        selected_employee_id = request.POST.get('select')
        

        print(selected_employee_id)
        newtask=project_task.objects.create(
            name=name,
            startDate=startDate,
            endDate=endDate,
            description=description,
            project_id=project,
            employee_id=employee.objects.get(pk= selected_employee_id)
            )
        newtask.save()
    
    return render(request,'create_task.html',{'employees':employees})
    



from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import employee
from .serializers import EmployeeSerializer

@api_view(['GET'])
def get_employee_data(request):
    if request.user.is_staff:
        employees = employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_project_data(request):
    if request.user.is_staff:
        projects = project_general.objects.all()
        serializer = project_generalSerializer(projects, many=True)
    return Response(serializer.data)

def react(request):
    return render(request, 'react.html')


class LoginView(APIView):
    
    def get(self, request, format=None):
        return render(request, 'login.html')

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            uname = serializer.validated_data['username']
            pwd = serializer.validated_data['password']
            user_authenticate = auth.authenticate(username=uname, password=pwd)
            
            if user_authenticate is not None:
                user = User.objects.get(username=uname)                
                data = employee.objects.get(username=user)
                auth.login(request, user_authenticate)
                print(data.position)
        
                if(data.position=='ai'or data.position=='software'):
                    return redirect('/',user='S')
                elif(data.position=='manager'):
                    return redirect('/',user='M')

            else:
                response_data = {
                 "message": "invalid username or password",
                    "data": None
                }
                return Response(response_data ,status=status.HTTP_401_UNAUTHORIZED)   
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class RegisterView(APIView):
    #get the register.html page
    def get(self, request, format=None):
        return render(request, 'register.html')

    #get user info entered in register.html 
    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        try:
            print('1')
            user = User.objects.get(username=username)
            print("3")
            return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_staff=True
            user.is_superuser=True
        
        
        serializer=EmployeeSerializer(data=request.data)
        
        if serializer.is_valid():
            user.is_active = True
            user.save()
            manager_group = Group.objects.get(name='manager')
            manager_group.user_set.add(user)
            position = 'manager'
            serializer.save(username=user,position=position)
            return redirect('login')
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def logout_view(request):
    logout(request)
    return redirect('/')
