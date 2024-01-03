# DRF imports
from rest_framework import generics,viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

# Django filters imports
from django_filters.rest_framework import DjangoFilterBackend

# Local model imports
from .models import ElevatorSystem,Elevator,ElevatorRequest

# Local serializers
from .serializers import ElevatorSystemSerializer,ElevatorSerializer,ElevatorRequestSerializer,ElevatorRequestSerializerAll

# App functions 
from .create_elevators import create_elevators



class ElevatorSystemList(generics.ListAPIView):
  '''
  Fetch all the listed elevator systems.
  '''
  queryset = ElevatorSystem.objects.all()
  serializer_class = ElevatorSystemSerializer


class CreateElevatorSystem(generics.CreateAPIView):
  '''
  Create a new elevator system.
  '''
  serializer_class = ElevatorSystemSerializer

  # Overriding the perform_create method of 'mixins.CreateModelMixin', Parent class of 'CreateAPIView'
  def perform_create(self, serializer):
    serializer.save()

    # Creating elevators needed for the system. For more details check create_elevators.py
    create_elevators(
      number_of_elevators=serializer.data['number_of_elevators'],
      system_id=serializer.data['id']
    )



class ElevatorsList(generics.ListAPIView):
  '''
  Given an elevator system list all the elevators and their status. 
  '''
  serializer_class = ElevatorSerializer

  def get_queryset(self):
    system_id = self.kwargs['id']
    queryset = Elevator.objects.filter(elevator_system__id = system_id)

    return queryset


class ViewSingleElevator(generics.RetrieveAPIView):
  '''
  Get details of a specific elevator, 
  given its elevator system and elevator number with URL
  '''
  serializer_class = ElevatorSerializer

  def  get_object(self):
    system_id = self.kwargs['id']
    elevator_number = self.kwargs['pk']

    queryset = Elevator.objects.filter(
      elevator_system__id = system_id,
      elevator_number = elevator_number
    )

    return queryset[0]



class UpdateSingleElevator(generics.UpdateAPIView):
  '''
  Update details of a specific elevator, 
  given its elevator system and elevator number with URL
  It can be done together with the previous view, 
  but repeated for better understanding.
  '''
  serializer_class = ElevatorSerializer

  def  get_object(self):
    system_id = self.kwargs['id']
    elevator_number = self.kwargs['pk']

    queryset = Elevator.objects.filter(
      elevator_system__id = system_id,
      elevator_number = elevator_number
    )

    return queryset[0]

  #overriding put method by patch
  def put(self, request, *args, **kwargs):
    return self.partial_update(request, *args, **kwargs)


class CreateElevatorRequest(generics.CreateAPIView):
  '''
  Create a new request for a specific elevator, 
  given its elevator system and elevator number with URL.
  The inputs of requested and destinatiom floor is sent with
  the form-data.
  '''
  serializer_class = ElevatorRequestSerializer

  # Overriding the perform_create method of 'mixins.CreateModelMixin', Parent class of 'CreateAPIView'
  def perform_create(self, serializer):
    system_id = self.kwargs['id']
    elevator_number = self.kwargs['pk']

    queryset = Elevator.objects.filter(
      elevator_system__id = system_id,
      elevator_number = elevator_number
    )
    elevator_object = queryset[0]

    serializer.save(elevator = elevator_object)
    
    
class ElevatorRequestList(generics.ListAPIView):
  '''
  List all the requests for a given elevator
  Requests already served can be filtered with is_active
  parameter set false

  '''
  serializer_class = ElevatorRequestSerializerAll
  filter_backends = [DjangoFilterBackend]
  filterset_fields = ['is_active']

  def get_queryset(self):
    system_id = self.kwargs['id']
    elevator_number = self.kwargs['pk']

    elevator_object = Elevator.objects.filter(
      elevator_system__id = system_id,
      elevator_number = elevator_number
    )

    queryset = ElevatorRequest.objects.filter(elevator = elevator_object[0])
    return queryset



class FetchDestination(APIView):
  '''
  Fetch the next destination floor for a given elevator
  '''
  def get(self, request,id,pk):
    system_id = id
    elevator_number = pk

    elevator_object = Elevator.objects.filter(
      elevator_system__id = system_id,
      elevator_number = elevator_number
    )

    requests_pending = ElevatorRequest.objects.filter(
      elevator = elevator_object[0],
      is_active = True,
    ).order_by('request_time')

    return_dict = {

    }

    if elevator_object.count() !=1:
      return_dict = {
        'running' : False,
        'details' : 'The Elevator number is incorrect'
      }
      
    elif not elevator_object[0].is_operational:
      return_dict = {
        'running' : False,
        'details' : 'The Elevator is not operational'
      }
    elif requests_pending.count() == 0:
      return_dict = {
        'running' : False,
        'details' : 'The Elevator is not running currently, No pending requests'
      }
    elif requests_pending[0].requested_floor == elevator_object[0].current_floor:
      return_dict = {
        'running' : True,
        'details' : str(requests_pending[0].destination_floor)
      }
    else:
      return_dict = {
        'running' : True,
        'details' : str(requests_pending[0].requested_floor)
      }

    return Response(return_dict)