from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .models import Submissions, Exif
from PIL import Image, ExifTags
from django.core.files import File
import io
from datetime import datetime
from PIL.ExifTags import TAGS, GPSTAGS
from fractions import Fraction
import decimal

# def get_decimal_from_dms(dms, ref):
#     degrees, minutes, seconds = [float(val.numerator) / float(val.denominator) for val in dms]
#     result = degrees + (minutes / 60.0) + (seconds / 3600.0)
#     if ref in ['S', 'W']:
#         result *= -1
#     return result

# def get_decimal_from_dms_altitude(dms, ref):
#     result = float(dms.numerator) / float(dms.denominator)
#     if ref == 1:
#         result *= -1
#     return result

# def get_exif_data(image):
#     raw_exif_data = image._getexif()
#     exif_data = {}
#     if raw_exif_data is not None:
#         for tag, value in raw_exif_data.items():
#             tag_name = TAGS.get(tag, tag)
#             if tag_name == 'DateTimeOriginal':
#                 exif_data[tag_name] = datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
#             elif tag_name in ['GPSLatitude', 'GPSLongitude']:
#                 ref = raw_exif_data.get(GPSTAGS.get(tag+1))  # 'N', 'S', 'E', 'W'
#                 exif_data[tag_name] = get_decimal_from_dms(value, ref)
#             elif tag_name == 'GPSAltitude':
#                 ref = raw_exif_data.get(GPSTAGS.get(tag+1))  # 0, 1
#                 exif_data[tag_name] = get_decimal_from_dms_altitude(value, ref)
#             elif isinstance(value, bytes):
#                 exif_data[tag_name] = value.decode('utf-8', 'ignore')
#             else:
#                 exif_data[tag_name] = value
#     return exif_data

def get_decimal_from_dms(dms, ref):
    # If the input is already in degrees format, just return it
    if isinstance(dms, (int, float)):
        result = float(dms)
    else:
        # Otherwise, convert from DMS (Degree/Minute/Second) to decimal format
        degrees, minutes, seconds = [float(val.numerator) / float(val.denominator) for val in dms]
        result = degrees + (minutes / 60.0) + (seconds / 3600.0)
    
    if ref in ['S', 'W']:
        result *= -1

    # Round to 3 decimal places
    result = round(result, 3)
    
    return result


def get_decimal_from_dms_altitude(dms, ref):
    # If the input is already in degrees format, just return it
    if isinstance(dms, (int, float)):
        result = float(dms)
    else:
        # Otherwise, convert from DMS (Degree/Minute/Second) to decimal format
        result = float(dms.numerator) / float(dms.denominator)
    
    if ref == 1:
        result *= -1

    # Round to 3 decimal places
    result = round(result, 3)
    
    return result


def get_exif_data(image):
    raw_exif_data = image._getexif()
    exif_data = {}
    if raw_exif_data is not None:
        for tag, value in raw_exif_data.items():
            tag_name = ExifTags.TAGS.get(tag, tag)
            if tag_name == 'DateTimeOriginal':
                exif_data[tag_name] = datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
            elif tag_name == 'GPSInfo':
                for t, val in value.items():
                    subtag_name = ExifTags.GPSTAGS.get(t, t)
                    if subtag_name in ['GPSLatitude', 'GPSLongitude']:
                        ref = value.get(1 if subtag_name == 'GPSLatitude' else 3)  # 'N', 'S', 'E', 'W'
                        exif_data[subtag_name] = get_decimal_from_dms(val, ref)
                    elif subtag_name == 'GPSAltitude':
                        ref = int.from_bytes(value.get(5), byteorder='big')  # 0, 1
                        exif_data[subtag_name] = get_decimal_from_dms_altitude(val, ref)
                        exif_data['GPSAltitudeRef'] = ref
                    else:
                        exif_data[subtag_name] = val
            elif isinstance(value, bytes):
                exif_data[tag_name] = value.decode('utf-8', 'ignore')
            else:
                exif_data[tag_name] = value
    return exif_data



class IndexView(generic.ListView):
    model = Submissions

class DetailView(generic.DetailView):
    model = Submissions

# class CreateView(generic.edit.CreateView):
#     model = Submissions
#     fields = '__all__'

# class UpdateView(generic.edit.UpdateView):
#     model = Submissions
#     fields = '__all__'

class DeleteView(generic.edit.DeleteView):
    model = Submissions
    success_url = reverse_lazy('mainapp:index')


class CreateView(generic.edit.CreateView):
    model = Submissions
    fields = '__all__'

    def form_valid(self, form):
        self.object = form.save()
        with Image.open(self.object.image.path) as img:
            exif_data = get_exif_data(img)
            if exif_data is not None:
                Exif.objects.create(
                    submission=self.object,
                    aperture_value=exif_data.get('ApertureValue'),
                    brightness_value=exif_data.get('BrightnessValue'),
                    date_time_original=exif_data.get('DateTimeOriginal'),
                    exposure_bias_value=exif_data.get('ExposureBiasValue'),
                    exposure_program=exif_data.get('ExposureProgram'),
                    exposure_time=exif_data.get('ExposureTime'),
                    f_number=exif_data.get('FNumber'),
                    iso=exif_data.get('ISOSpeedRatings'),
                    max_aperture_value=exif_data.get('MaxApertureValue'),
                    metering_mode=exif_data.get('MeteringMode'),
                    shutter_speed_value=exif_data.get('ShutterSpeedValue'),
                    gps_altitude=exif_data.get('GPSAltitude'),
                    gps_altitude_ref=exif_data.get('GPSAltitudeRef'),
                    gps_latitude=exif_data.get('GPSLatitude'),
                    gps_latitude_ref=exif_data.get('GPSLatitudeRef'),
                    gps_longitude=exif_data.get('GPSLongitude'),
                    gps_longitude_ref=exif_data.get('GPSLongitudeRef'),
                    make=exif_data.get('Make'),
                    model=exif_data.get('Model'),
                    lens_make=exif_data.get('LensMake'),
                    lens_model=exif_data.get('LensModel'),
                    exposure_time_star=exif_data.get('ExposureTime'),
                    f_number_star=exif_data.get('FNumber'),
                    iso_star=exif_data.get('ISOSpeedRatings'),
                    focal_length_star=exif_data.get('FocalLength')
                )
        return super().form_valid(form)


class UpdateView(generic.edit.UpdateView):
    model = Submissions
    fields = '__all__'

    def form_valid(self, form):
        self.object = form.save()
        with Image.open(self.object.image.path) as img:
            exif_data = get_exif_data(img)
            if exif_data is not None:
                Exif.objects.create(
                    submission=self.object,
                    aperture_value=exif_data.get('ApertureValue'),
                    brightness_value=exif_data.get('BrightnessValue'),
                    date_time_original=exif_data.get('DateTimeOriginal'),
                    exposure_bias_value=exif_data.get('ExposureBiasValue'),
                    exposure_program=exif_data.get('ExposureProgram'),
                    exposure_time=exif_data.get('ExposureTime'),
                    f_number=exif_data.get('FNumber'),
                    iso=exif_data.get('ISOSpeedRatings'),
                    max_aperture_value=exif_data.get('MaxApertureValue'),
                    metering_mode=exif_data.get('MeteringMode'),
                    shutter_speed_value=exif_data.get('ShutterSpeedValue'),
                    gps_altitude=exif_data.get('GPSAltitude'),
                    gps_altitude_ref=exif_data.get('GPSAltitudeRef'),
                    gps_latitude=exif_data.get('GPSLatitude'),
                    gps_latitude_ref=exif_data.get('GPSLatitudeRef'),
                    gps_longitude=exif_data.get('GPSLongitude'),
                    gps_longitude_ref=exif_data.get('GPSLongitudeRef'),
                    make=exif_data.get('Make'),
                    model=exif_data.get('Model'),
                    lens_make=exif_data.get('LensMake'),
                    lens_model=exif_data.get('LensModel'),
                    exposure_time_star=exif_data.get('ExposureTime'),
                    f_number_star=exif_data.get('FNumber'),
                    iso_star=exif_data.get('ISOSpeedRatings'),
                    focal_length_star=exif_data.get('FocalLength')
                )
        return super().form_valid(form)
