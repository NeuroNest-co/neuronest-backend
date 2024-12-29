from django.db import models
from django.utils.timezone import now

class Patient(models.Model):
    patientId = models.AutoField(primary_key=True)
    age = models.PositiveIntegerField()
    date = models.DateTimeField(default=now)
    doctor_comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.patientId

