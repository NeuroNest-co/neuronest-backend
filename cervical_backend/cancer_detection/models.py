from django.db import models
from django.utils.timezone import now

class Patient(models.Model):
    patientId = models.AutoField(primary_key=True)
    age = models.PositiveIntegerField()
    date = models.DateTimeField(default=now)
    doctor_comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Patient {self.patientId} - {self.date.strftime('%Y-%m-%d %H:%M:%S')}"


class apiResponse(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    response_data = models.JSONField()
    full_response = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
