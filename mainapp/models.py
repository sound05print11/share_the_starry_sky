from django.db import models

class Submissions(models.Model):
    username = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/')
    comment = models.TextField()

class Exif(models.Model):
    camera_manufacturer_and_model = models.CharField(max_length=200, blank=True)
    image_capture_date = models.DateTimeField(null=True, blank=True)
    shutter_speed = models.FloatField(null=True, blank=True)
    exposure_time = models.FloatField(null=True, blank=True)
    aperture_value = models.FloatField(null=True, blank=True)
    iso_sensitivity = models.IntegerField(null=True, blank=True)
    focal_length = models.FloatField(null=True, blank=True)
    metering_mode = models.CharField(max_length=200, blank=True)
    flash_usage = models.BooleanField(null=True, blank=True)
    image_resolution = models.CharField(max_length=200, blank=True)
    image_orientation = models.CharField(max_length=200, blank=True)
    lens_type = models.CharField(max_length=200, blank=True)
    white_balance_setting = models.CharField(max_length=200, blank=True)
    digital_zoom_ratio = models.FloatField(null=True, blank=True)
    focal_length_in_35mm_film = models.IntegerField(null=True, blank=True)
    scene_capture_type = models.CharField(max_length=200, blank=True)
    gps_info_latitude = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    gps_info_longitude = models.DecimalField(max_digits=9, decimal_places=3, null=True, blank=True)
    gps_info_altitude = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    submission = models.ForeignKey(Submissions, on_delete=models.CASCADE, related_name="exif_data")
