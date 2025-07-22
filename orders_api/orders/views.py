from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, filters
from .models import Order
from .serializers import OrderSerializer
from rest_framework.pagination import PageNumberPagination

class OrderPagination(PageNumberPagination):
    page_size = 10

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related('customer').prefetch_related('tracking_events').all()
    serializer_class = OrderSerializer
    pagination_class = OrderPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['status', 'customer__name']
