from rest_framework import serializers
from .models import Customer, Order, OrderTrackingEvent

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class OrderTrackingEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderTrackingEvent
        fields = '__all__'
        read_only_fields = ['timestamp']


class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    tracking_events = OrderTrackingEventSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        

    def create(self, validated_data):
        customer_data = validated_data.pop('customer')
        customer, _ = Customer.objects.get_or_create(**customer_data)
        order = Order.objects.create(customer=customer, **validated_data)
        OrderTrackingEvent.objects.create(order=order, status=order.status, comment='Order created.')
        return order
    

    def update(self, instance, validated_data):
        if 'status' in validated_data:
            new_status = validated_data['status']
            valid_transitions = {
                'CREATED': 'PICKED',
                'PICKED': 'DELIVERED'
            }
            if instance.status != new_status:
                if valid_transitions.get(instance.status) != new_status:
                    raise serializers.ValidationError(f"Invalid status transition from {instance.status} to {new_status}")
                OrderTrackingEvent.objects.create(order=instance, status=new_status, comment='Status updated.')
        return super().update(instance, validated_data)
