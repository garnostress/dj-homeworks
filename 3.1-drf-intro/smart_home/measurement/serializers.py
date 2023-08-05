from rest_framework import serializers
from .models import Measurement, Sensor

# TODO: опишите необходимые сериализаторы

class MeasurementSerializer(serializers.ModelSerializer):
    # sensor_id = serializers.IntegerField()
    # temperature = serializers.DecimalField(max_digits=4, decimal_places=2)
    # created_at = serializers.DateField()
    # image = serializers.ImageField()
    
    class Meta:
        model = Measurement
        fields = ['temperature', 'created_at']
        
    # def create(self, validated_data):
    #    return Measurement.objects.create(**validated_data)
     

class SensorDetailSerializer(serializers.ModelSerializer):
    measurements = MeasurementSerializer(read_only=True, many=True)
    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description', 'measurements']