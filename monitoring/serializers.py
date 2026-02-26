from rest_framework import serializers
from .models import WaterQualityReading

class WaterQualitySerializer(serializers.ModelSerializer):

    class Meta:
        model = WaterQualityReading
        fields = '__all__'
        read_only_fields = ['predicted_do']

    # Validation rules
    def validate_temperature(self, value):
        if value < 0 or value > 50:
            raise serializers.ValidationError("Temperature must be between 0 and 50°C.")
        return value

    def validate_ph(self, value):
        if value < 0 or value > 14:
            raise serializers.ValidationError("pH must be between 0 and 14.")
        return value

    def validate_light_intensity(self, value):
        if value < 0:
            raise serializers.ValidationError("Light intensity cannot be negative.")
        return value

    # Updated DO prediction formula (includes light)
    def create(self, validated_data):
        temp = validated_data['temperature']
        ph = validated_data['ph']
        turbidity = validated_data['turbidity']
        light = validated_data['light_intensity']

        # Improved prediction formula
        predicted_do = (
            14.6
            - (0.4 * temp)
            - (0.1 * turbidity)
            + (0.2 * ph)
            - (0.0005 * light)  # Light slightly affects DO
        )

        validated_data['predicted_do'] = round(predicted_do, 2)

        return super().create(validated_data)