import os
from django.db import models
from django.conf import settings

def csv_file_path(instance, filename):
    return os.path.join('csvfiles', filename)

class CSVFile(models.Model):
    file_name = models.CharField(max_length=255)
    file = models.FileField(upload_to=csv_file_path)

    def __str__(self):
        return str(self.file_name)


    def delete(self, *args, **kwargs):
        if self.file:
            path = os.path.join(settings.MEDIA_ROOT, 'csvfiles', str(self.file))
            if os.path.exists(path):
                os.remove(path)
        super().delete(*args, **kwargs)