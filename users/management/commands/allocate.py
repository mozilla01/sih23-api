from django.core.management.base import BaseCommand
import time
import math
from colorama import Fore, Style
import geopy.distance
from users.models import Rake, CompanyAccount, ConsumerAccount
from django.db import transaction

earth_radius = 6371.0

rake_capacity = 10


# Gets the next location
def interpolate_coordinates(lat1, lon1, lat2, lon2, distance_km):
    # Convert latitude and longitude from degrees to radians
    new_lat1, new_lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Calculate the angular distance between the two points
    angular_distance = 2 * math.asin(math.sqrt(
        math.sin((lat2 - new_lat1) / 2) ** 2 +
        math.cos(new_lat1) * math.cos(lat2) * math.sin((lon2 - new_lon1) / 2) ** 2
    ))

    if angular_distance == 0:
        # Points are nearly identical; return one of the points
        return "{},{}".format(lat1, lon1)

    # Calculate the fractional distance to the interpolated point
    fraction = distance_km / (earth_radius * angular_distance)

    # Calculate the coordinates of the interpolated point
    interpolated_lat = math.degrees(new_lat1 + fraction * (lat2 - new_lat1))
    interpolated_lon = math.degrees(new_lon1 + fraction * (lon2 - new_lon1))

    print("New coords are {} and {}".format(interpolated_lat, interpolated_lon))

    return "{},{}".format(interpolated_lat, interpolated_lon)


def reducer():
    rakes = Rake.objects.filter(status="busy")
    for r in rakes:
        rake = Rake.objects.get(id=r.id)
        print("Rake source id is {}".format(r.source))
        source = CompanyAccount.objects.get(id=r.source)
        consumer = ConsumerAccount.objects.get(id=r.destination)
        if r.distance <= 0:
            print("Rake {} has reached destination".format(r.id))
            # Fetch source and set it to unallocated
            source.allocated = False
            source.save()

            rake.status = "free"
            print("Consumer location is {}".format(consumer.location))
            print("Rake location is {}".format(rake.location))
            rake.location = consumer.location
            rake.source = None
            rake.destination = None
            print("Rake has reach destination, location: {}".format(rake.location))
            rake.save()

        if r.distance > 0:
            rake.distance -= 10
            print("Rake location is {}".format(rake.location))
            rake.location = interpolate_coordinates(
                float(r.location.split(",")[0]),
                float(r.location.split(",")[1]),
                float(consumer.location.split(",")[0]),
                float(consumer.location.split(",")[1]),
                10,
            )
            print("Distance left for rake {}: {}".format(r.id, r.distance))
            print("Rake is travelling, location: {}".format(rake.location))
            rake.save()


def remover(arr, id):
    for i in arr:
        if i.id == id:
            arr.remove(i)


def distance(x1, y1, x2, y2):
    return geopy.distance.geodesic([x1, y1], [x2, y2]).km


def check_stock(arr, capacity):
    print("Checking stock")
    shortlisted = []
    for i in arr:
        if i.stock >= capacity and i.allocated is False:
            shortlisted.append(i)

    return shortlisted


def check_free_rakes(arr):
    print("Checking free rakes")
    shortlisted = []
    for i in arr:
        if i.status == "free":
            shortlisted.append(i)

    return shortlisted


def min_distance(shortlisted_sources, shortlisted_rakes):
    print(len(shortlisted_sources))
    while len(shortlisted_sources) > 0 and len(shortlisted_rakes) > 0:
        min_dist = 1000000
        source_id = -1
        rake_id = -1
        for i in shortlisted_rakes:
            for j in shortlisted_sources:
                consumer = ConsumerAccount.objects.get(id=j.consumer.id)
                previous_val = min_dist
                dist = distance(
                    float(i.location.split(",")[0]),
                    float(i.location.split(",")[1]),
                    float(j.location.split(",")[0]),
                    float(j.location.split(",")[1]),
                ) + distance(
                    float(j.location.split(",")[0]),
                    float(j.location.split(",")[1]),
                    float(consumer.location.split(",")[0]),
                    float(consumer.location.split(",")[1]),
                )
                print(
                    "{} is the distance from rake {} to source {} to consumer {}".format(dist, i.id, j.id,
                                                                                         j.consumer))
                min_dist = min(
                    dist,
                    min_dist,
                )
                if min_dist != previous_val:
                    source_id = j.id
                    rake_id = i.id

        values = {
            "id": rake_id,
            "status": "busy",
            "source_id": source_id,
            "distance": min_dist,
        }
        change(values)
        remover(shortlisted_rakes, rake_id)
        remover(shortlisted_sources, source_id)
        print(
            Fore.GREEN + "Rake {} will travel to source S{}".format(rake_id, source_id)
        )
        print(Style.RESET_ALL)


def change(values):
    print("Source ID is {}".format(values["source_id"]))
    print("Rake ID is {}".format(values["id"]))

    with transaction.atomic():
        source = CompanyAccount.objects.get(id=values["source_id"])
        rake = Rake.objects.get(id=values["id"])

        # update source
        source.allocated = True
        source.stock -= rake_capacity
        source.save()

        # update rake
        rake.status = values["status"]
        rake.source = source.id
        rake.destination = source.consumer.id
        rake.distance = values["distance"]
        rake.save()


class Command(BaseCommand):
    help = "Runs the allocation algorithm"

    def handle(self, *args, **options):
        while True:
            rakes = Rake.objects.all()
            sources = CompanyAccount.objects.all()
            free_sources = check_stock(sources, rake_capacity)
            free_rakes = check_free_rakes(rakes)
            print("Iterating")
            min_distance(free_sources, free_rakes)
            reducer()
            time.sleep(1)
            for s in sources:
                if s.stock < 20:
                    source = CompanyAccount.objects.get(id=s.id)
                    source.stock = source.stock + 0.2
                    source.save()
