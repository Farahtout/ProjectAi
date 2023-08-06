from django.db import models
from django.contrib.auth.models import User 
from django.core.exceptions import ValidationError
from decimal import Decimal

class employee(models.Model):
    POSITION_CHOICES = (
        ('software', ' Software'),
        ('ai', 'Ai'),
        ('manager','Manager')
    )
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    FirstName=models.CharField(max_length=20)
    LastName=models.CharField(max_length=20)
    email=models.EmailField(unique=True)
    address= models.CharField(max_length=20)
    birthday = models.DateField(null=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,default='M')
    certification=models.CharField(max_length=20,null=True)
    position=models.CharField(max_length=20, choices=POSITION_CHOICES, default='ai')
   
    

    def __str__(self):
         return self.FirstName
    
    def Get_All_Projects(self):
        return self.project_general_set.all()

    def Get_All_tasks(self):
        return self.project_task_set.all()





class project_general(models.Model):
    STATUS_CHOICES = (
        ('completed', 'Completed'),
        ('panding', ' Panding'),
        ('cancelled', 'Cancelled'),
    )
    TYPE_CHOICES = (
        ('ai', 'Ai'),
        ('other', 'Other'),
    )
    name=models.CharField(max_length=50)
    startDate = models.DateField()
    endDate = models.DateField()
    description=models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='panding')
    employees = models.ManyToManyField(employee)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='other')
    cost = models.DecimalField(max_digits=10, decimal_places=2, default="0")
    def clean(self):
        if self.endDate < self.startDate:
            raise ValidationError({'endDate': "End date must be later than start date."})
        elif  not isinstance(self.cost, Decimal) or self.cost<0:
           raise ValidationError({"the cost should be an digit positif"})


   



    def __str__(self):
        return self.name

    def Get_All_Project_Tasks(self):
        return self.project_task_set.all()

    
        


class project_task(models.Model):
    name=models.CharField(max_length=50)
    startDate = models.DateField()
    endDate = models.DateField()
    description=models.CharField(max_length=200)
    project_id=models.ForeignKey(project_general, on_delete=models.CASCADE)
    employee_id= models.ForeignKey(employee, on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.name


    




    


