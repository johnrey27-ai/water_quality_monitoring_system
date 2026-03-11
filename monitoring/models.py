from django.db import models

class WaterQualityReading(models.Model):
    temperature = models.FloatField()
    ph = models.FloatField()
    turbidity = models.FloatField()
    light_intensity = models.FloatField()
    predicted_do = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reading at {self.timestamp}"