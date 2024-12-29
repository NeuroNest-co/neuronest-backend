from django.db import models
from django.utils.timezone import now

class Patient(models.Model):
    patientId = models.AutoField(primary_key=True)
    age = models.PositiveIntegerField()
    date = models.DateTimeField(default=now)
    doctor_comment = models.TextField(blank=True, null=True)

    def __str__(self):
        # Return patientId and date in string format for better representation
        return f"Patient {self.patientId} - {self.date.strftime('%Y-%m-%d %H:%M:%S')}"
