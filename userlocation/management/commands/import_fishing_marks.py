import csv
from userlocation.models import Fishingmark
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point

class Command(BaseCommand):
    help = 'Import fishing mark data from a fishing_marks.csv file'

    def handle(self, *args, **options):
        csv_file = "fishing_marks.csv"

        # delete all existing fishingmark data
        Fishingmark.objects.all().delete()

        with open(csv_file, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                latitude = float(row["lat"])
                longitude = float(row["lon"])
                description = row["description"]
                map_point = Point((longitude, latitude), srid=4326)

                fishingmark = Fishingmark(
                    latitude=latitude,
                    longitude=longitude,
                    description=description,
                    location = map_point
                )
                fishingmark.save()

        print("Successfully imported fishing marks")
