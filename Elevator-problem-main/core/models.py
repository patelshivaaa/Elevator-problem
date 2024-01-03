# Django imports
from django.db import models


class ElevatorSystem(models.Model):
  '''
  Elevator system Model. Equivalent to a building containing a number of elevators
  Also contains the default ID parameter assigned by django as a primary key.
  Used to make the project compatible with multiple elevator systems.
  Minimum floor is assumed as 0 but dynamic minimum floor can be implemented easily.

  '''
  system_name = models.CharField(max_length = 20)
  max_floor = models.IntegerField()
  number_of_elevators = models.PositiveSmallIntegerField()

  def __str__(self) -> str:
    return_str = str(self.system_name) + " Elevator System No " + str(self.id)
    return return_str


class Elevator(models.Model):
  '''
  Elevator object model. Represents a single elevator that can move up and down. It
  is always a part of an entire elevator system. So elevator system is assigned as foreignkey.
  
  '''

  # Django integerchoicefield
  class RunningStatus(models.IntegerChoices):
    '''
    Choices for running status of the elevator system
    '''
    GOING_UP = 1
    STANDING_STILL = 0
    GOING_DOWN = -1

  elevator_system = models.ForeignKey(ElevatorSystem , on_delete=models.CASCADE)

  elevator_number = models.IntegerField()
  current_floor = models.PositiveSmallIntegerField(default=0)

  is_operational = models.BooleanField(default=True)
  is_door_open = models.BooleanField(default=True)
  running_status = models.IntegerField(choices=RunningStatus.choices,default=0)


  def __str__(self) -> str:
    return_str = "Elevator Number" + str(self.elevator_number)
    return return_str



class ElevatorRequest(models.Model):
  '''
  User request targeted to a specific elevator. This can be improved further using model managers 
  to clean the invalid requests like request elevator in negative floor/greater than maximum floor
  request an elevator that doesn't exist.
  '''

  elevator = models.ForeignKey(Elevator, on_delete=models.CASCADE)
  requested_floor = models.PositiveSmallIntegerField()
  destination_floor = models.PositiveSmallIntegerField()
  request_time = models.DateTimeField(auto_now_add=True)
  is_active = models.BooleanField(default=True)

  def __str__(self) -> str:
    return_str = str(self.elevator) + " is Requested at floor " + str(self.requested_floor)
    return return_str
