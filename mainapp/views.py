from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .models import Submissions, Exif
from PIL import Image, ExifTags
from django.core.files import File
import io
from datetime import datetime

class IndexView(generic.ListView):
    model = Submissions

class DetailView(generic.DetailView):
    model = Submissions

# class CreateView(generic.edit.CreateView):
#     model = Submissions
#     fields = '__all__'

class UpdateView(generic.edit.UpdateView):
    model = Submissions
    fields = '__all__'

class DeleteView(generic.edit.DeleteView):
    model = Submissions
    success_url = reverse_lazy('mainapp:index')

class CreateView(generic.edit.CreateView):
    model = Submissions
    fields = '__all__'

    def form_valid(self, form):
        response = super().form_valid(form)

        # Get the newly created Submissions object
        submission = self.object

        # Open the uploaded image file
        image = Image.open(submission.image.path)

        # Get the EXIF data (if any)
        exif_data = image._getexif()

        if exif_data is not None:
            exif = {
                ExifTags.TAGS[k]: v
                for k, v in exif_data.items()
                if k in ExifTags.TAGS and isinstance(ExifTags.TAGS[k], str)
            }

            exif_instance = Exif()

            # Extract needed fields from exif_data and save them in an Exif object
            try:
                exif_instance.make = exif.get('Make', '')
                exif_instance.model = exif.get('Model', '')
                exif_instance.datetimeoriginal = exif.get('DateTimeOriginal', '')
                exif_instance.exposuretime = exif.get('ExposureTime', '')
                exif_instance.fnumber = exif.get('FNumber', '')
                exif_instance.isospeedratings = exif.get('ISOSpeedRatings', '')
                exif_instance.focallength = exif.get('FocalLength', '')
                exif_instance.meteringmode = exif.get('MeteringMode', '')
                exif_instance.flash = exif.get('Flash', '')
                exif_instance.xresolution = exif.get('XResolution', '')
                exif_instance.yresolution = exif.get('YResolution', '')
                exif_instance.orientation = exif.get('Orientation', '')
                exif_instance.lensmodel = exif.get('LensModel', '')
                exif_instance.lensspecification = exif.get('LensSpecification', '')
                exif_instance.whitebalance = exif.get('WhiteBalance', '')
                exif_instance.digitalzoomratio = exif.get('DigitalZoomRatio', '')
                exif_instance.focallengthin35mmfilm = exif.get('FocalLengthIn35mmFilm', '')
                exif_instance.scenecapturetype = exif.get('SceneCaptureType', '')
                exif_instance.gpslatitude = exif.get('GPSLatitude', None)
                exif_instance.gpslongitude = exif.get('GPSLongitude', None)
                exif_instance.gpsaltitude = exif.get('GPSAltitude', None)

                # Set relation to the submission
                exif_instance.submission = submission

                # Save the Exif object
                exif_instance.save()

            except Exception as e:
                print(f"Error while saving EXIF data: {e}")
              
        return response
