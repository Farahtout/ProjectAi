from django.contrib import admin
from .models import project_general, employee , project_task
# Register your models here.
from django.contrib import admin

# Register your models here.
from django.contrib import admin




class employeeAdmin(admin.ModelAdmin):
  


    def get_queryset(self, request):
        
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            
            return qs
        try:
            if request.user.employee :
                return qs.filter(employee=request.user.employee)
        except:
            pass

        return qs.none()


admin.site.register(employee, employeeAdmin)

admin.site.register(project_general)

admin.site.register(project_task)