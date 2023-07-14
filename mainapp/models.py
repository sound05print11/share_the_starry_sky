from django.db import models
from django.urls import reverse
from PIL import Image

class Submissions(models.Model):
    username = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/')
    comment = models.TextField()

    def get_absolute_url(self):
        return reverse('mainapp:detail', kwargs={'pk': self.pk})

# class Exif(models.Model):
#     exif_data = models.TextField(blank=True)  # new field for all exif data
#     submission = models.ForeignKey(Submissions, on_delete=models.CASCADE, related_name="exif_data")

from django.db import models

class Exif(models.Model):
    submission = models.ForeignKey(Submissions, on_delete=models.CASCADE, related_name="exif_data", null=True)
    # 撮影に関する情報の主なタグ名
    aperture_value = models.FloatField(blank=True, null=True)
    brightness_value = models.FloatField(blank=True, null=True)
    date_time_original = models.DateTimeField(blank=True, null=True)
    exposure_bias_value = models.FloatField(blank=True, null=True)
    exposure_program = models.IntegerField(blank=True, null=True)
    exposure_time = models.FloatField(blank=True, null=True)
    f_number = models.FloatField(blank=True, null=True)
    iso = models.IntegerField(blank=True, null=True)
    max_aperture_value = models.FloatField(blank=True, null=True)
    metering_mode = models.IntegerField(blank=True, null=True)
    shutter_speed_value = models.FloatField(blank=True, null=True)

    # GPS情報の主なタグ名
    gps_altitude = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    gps_altitude_ref = models.IntegerField(blank=True, null=True)
    gps_latitude = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    gps_latitude_ref = models.CharField(max_length=1, blank=True, null=True)
    gps_longitude = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    gps_longitude_ref = models.CharField(max_length=1, blank=True, null=True)

    # 機材構成に関する主なタグ名
    make = models.CharField(max_length=255, blank=True, null=True)
    model = models.CharField(max_length=255, blank=True, null=True)
    lens_make = models.CharField(max_length=255, blank=True, null=True)
    lens_model = models.CharField(max_length=255, blank=True, null=True)

    # 星空を撮影する際に重要なタグ名
    exposure_time_star = models.FloatField(blank=True, null=True)
    f_number_star = models.FloatField(blank=True, null=True)
    iso_star = models.IntegerField(blank=True, null=True)
    focal_length_star = models.FloatField(blank=True, null=True)

