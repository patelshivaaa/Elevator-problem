from django.contrib import admin
from .models import ElevatorSystem,Elevator

class ElevatorAdmin(admin.StackedInline):
    model = Elevator


# Register Elevators under an elevator system in the admin panel
class ElevatorSystemAdmin(admin.ModelAdmin):
    inlines = [ElevatorAdmin]

admin.site.register(ElevatorSystem,ElevatorSystemAdmin)