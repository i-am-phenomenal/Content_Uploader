from django.db import models
import uuid
from contentUploader import settings
from .signals import validate_file_type
from django.db.models import signals

    
class ConvertedFilePath(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    convertedFilePath = models.CharField(max_length=100)


class File(models.Model): 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fileName = models.CharField(max_length=50)
    fileType =  models.CharField(max_length=20, choices=[("Image", "Image"), ("Video", "Video")], default="Image")
    fileObject = models.FileField(null=False, blank=False, upload_to=settings.MEDIA_ROOT)
    fileSize = models.CharField(max_length=100, default=0)
    fileFormat = models.CharField(null=True, blank=True, max_length=10, default="") 
    convertedFilePaths = models.CharField(max_length=500)
    fileResolution = models.IntegerField(default=360)

    insertedAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now=True)

signals.pre_save.connect(receiver=validate_file_type, sender=File)