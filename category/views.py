from django.shortcuts import render
from rest_framework import generics
from .models import Category
from .serializers import CategorySerializer
from rest_framework import permissions
# Create your views here.

class CategoryCreateListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = (permissions.IsAdminUser(),) # or [permissions.IsAdminUser()]

    def get_permissions(self):
        if self.request.method == 'POST':
            return permissions.IsAdminUser(), 
        return permissions.AllowAny(),


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'

    def get_permissions(self):
        if self.request.method =='GET':
            return permissions.AllowAny(),
        return permissions.IsAdminUser(),
 


