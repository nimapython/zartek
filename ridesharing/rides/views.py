from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from rides.models import Ride
from .serializers import RideSerializer, UserSerializer

class UserViewSet(ViewSet):
    permission_classes = [AllowAny]  # Allow access to all users

    # Registration method
    def register(self, request):
        # Using the updated serializer with additional fields
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Create the user and generate the token
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "message": "User registered successfully.",
                    "user": serializer.data,
                    "token": token.key,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Login method
    def login(self, request):
        # Authenticate the user based on username and password
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {"message": "Login successful", "token": token.key},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [AllowAny]  # Require authentication for accessing these endpoints

    def create(self, request, *args, **kwargs):
        """ Create a new ride request. """
        rider = request.user  # The user who is authenticated is the rider
        driver = request.data.get('driver')
        pickup_location = request.data.get('pickup_location')
        dropoff_location = request.data.get('dropoff_location')

        # Validate the incoming data
        if not driver or not pickup_location or not dropoff_location:
            return Response(
                {"message": "Missing required fields."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create a new ride instance
        ride = Ride.objects.create(
            rider=rider,
            driver_id=driver,
            pickup_location=pickup_location,
            dropoff_location=dropoff_location
        )

        serializer = RideSerializer(ride)
        return Response(
            {"message": "Ride request created successfully", "ride": serializer.data},
            status=status.HTTP_201_CREATED
        )
    
    def list(self, request, *args, **kwargs):
        """ List allf rides """
        queryset = Ride.objects.all()
        serializer = RideSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        """ Get details of a specific ride """
        ride = self.get_object()
        serializer = RideSerializer(ride)
        return Response(serializer.data)