from django.db import models
from auction.validators import validate_file_size


class Slider(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="slider/images", validators=[validate_file_size])
    url = models.URLField(max_length=500)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']