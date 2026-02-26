from rest_framework import serializers
from .models import WaterQualityReading


class WaterQualitySerializer(serializers.ModelSerializer):

    class Meta:
        model = WaterQualityReading
        fields = '__all__'
        read_only_fields = ['predicted_do']

    # -------------------------
    # Field-level validations
    # -------------------------

    def validate_temperature(self, value):
        if not 0 <= value <= 50:
            raise serializers.ValidationError(
                "Temperature must be between 0 and 50°C."
            )
        return value

    def validate_ph(self, value):
        if not 0 <= value <= 14:
            raise serializers.ValidationError(
                "pH must be between 0 and 14."
            )
        return value

    def validate_light_intensity(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Light intensity cannot be negative."
            )
        return value

    def validate_turbidity(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Turbidity cannot be negative."
            )
        return value

    # -------------------------
    # Object-level validation
    # -------------------------

    def validate(self, attrs):
        """
        Additional system-wide validation.
        Prevent unrealistic environmental combinations.
        """
        if attrs['temperature'] > 40 and attrs['dissolved_oxygen'] if 'dissolved_oxygen' in attrs else False:
            raise serializers.ValidationError(
                "High temperature readings typically result in low dissolved oxygen."
            )
        return attrs

    # -------------------------
    # DO Prediction Logic
    # -------------------------

    def calculate_do(self, temp, ph, turbidity, light):
        """
        Encapsulated DO prediction formula.
        Easier to maintain and test.
        """
        predicted_do = (
            14.6
            - (0.4 * temp)
            - (0.1 * turbidity)
            + (0.2 * ph)
            - (0.0005 * light)
        )

        # DO cannot be negative
        return round(max(predicted_do, 0), 2)

    def create(self, validated_data):
        temp = validated_data['temperature']
        ph = validated_data['ph']
        turbidity = validated_data['turbidity']
        light = validated_data['light_intensity']

        validated_data['predicted_do'] = self.calculate_do(
            temp, ph, turbidity, light
        )

        return super().create(validated_data)