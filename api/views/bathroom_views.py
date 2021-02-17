from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token

from ..models.bathroom import Bathroom
from ..serializers import BathroomSerializer, UserSerializer

# Create your views here.
class Bathrooms(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = BathroomSerializer
    def get(self, request):
        """Index request"""
        # Get all the bathrooms:
        # bathrooms = Bathroom.objects.all()
        # Filter the bathrooms by owner, so you can only see your owned bathrooms
        bathrooms = Bathroom.objects.filter(owner=request.user.id)
        # Run the data through the serializer
        data = BathroomSerializer(bathrooms, many=True).data
        return Response({ 'bathrooms': data })

    def post(self, request):
        """Create request"""
        # Add user to request data object
        request.data['bathroom']['owner'] = request.user.id
        # Serialize/create bathroom
        bathroom = BathroomSerializer(data=request.data['bathroom'])
        # If the mango data is valid according to our serializer...
        if bathroom.is_valid():
            # Save the created mango & send a response
            bathroom.save()
            return Response({ 'bathroom': bathroom.data }, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        return Response(bathroom.errors, status=status.HTTP_400_BAD_REQUEST)

class BathroomDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        # Locate the bathroom to show
        bathroom = get_object_or_404(Bathroom, pk=pk)
        # Only want to show owned bathrooms?
        if not request.user.id == bathroom.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this bathroom')

        # Run the data through the serializer so it's formatted
        data = BathroomSerializer(bathroom).data
        return Response({ 'bathroom': data })

    def delete(self, request, pk):
        """Delete request"""
        # Locate bathroom to delete
        bathroom = get_object_or_404(Bathroom, pk=pk)
        # Check the bathroom's owner agains the user making this request
        if not request.user.id == bathroom.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this mango')
        # Only delete if the user owns the  bathroom
        bathroom.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""
        # Remove owner from request object
        # This "gets" the owner key on the data['bathroom'] dictionary
        # and returns False if it doesn't find it. So, if it's found we
        # remove it.
        if request.data['bathroom'].get('owner', False):
            del request.data['bathroom']['owner']

        # Locate Mango
        # get_object_or_404 returns a object representation of our Bathroom
        bathroom = get_object_or_404(Bathroom, pk=pk)
        # Check if user is the same as the request.user.id
        if not request.user.id == bathroom.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this bathroom')

        # Add owner to data object now that we know this user owns the resource
        request.data['bathroom']['owner'] = request.user.id
        # Validate updates with serializer
        data = BathroomSerializer(bathroom, data=request.data['bathroom'])
        if data.is_valid():
            # Save & send a 204 no content
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
