import time
import json
import math
from colorama import Fore, Style
import geopy.distance


earth_radius = 6371.0


# Gets the next location
def interpolate_coordinates(lat1, lon1, lat2, lon2, distance_km):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Calculate the angular distance between the two points
    angular_distance = 2 * math.asin(math.sqrt(
        math.sin((lat2 - lat1) / 2) ** 2 +
        math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    ))

    if angular_distance == 0:
        # Points are nearly identical; return one of the points
        return lat1, lon1

    # Calculate the fractional distance to the interpolated point
    fraction = distance_km / (earth_radius * angular_distance)

    # Calculate the coordinates of the interpolated point
    interpolated_lat = math.degrees(lat1 + fraction * (lat2 - lat1))
    interpolated_lon = math.degrees(lon1 + fraction * (lon2 - lon1))

    return [interpolated_lat, interpolated_lon]

def reducer(rakes):
    for r in rakes:
        if r["distance"] <= 0 and r["status"] == "busy":
            print("Rake {} has reached destination".format(r["id"]))
            sources[r["source"] - 1]["allocated"] = False
            r["status"] = "free"
            r["location"] = consumers[r["destination"] - 1]["location"]
            r["source"] = None
            r["destination"] = None

        if r["distance"] > 0:
            r["distance"] -= 10
            r["location"] = interpolate_coordinates(
                r["location"][0],
                r["location"][1],
                consumers[r["destination"] - 1]["location"][0],
            consumers[r["destination"] - 1]["location"][1],
                10,
            )
            print("Distance left for rake {}: {}".format(r["id"], r["distance"]))


def remover(arr, id):
    for i in arr:
        if i["id"] == id:
            arr.remove(i)


def distance(x1, y1, x2, y2):
    return geopy.distance.geodesic([x1, y1], [x2, y2]).km

global data
with open('sample.json', 'r') as rfile:
    data = json.load(rfile)

rakes = data["rakes"]

rake_capacity = data["rake_capacity"]

sources = data["sources"]
consumers = data["consumers"]


def check_stock(arr, capacity):
    print("Checking stock")
    shortlisted = []
    for i in arr:
        if i["stock"] >= capacity and i["allocated"] == False:
            shortlisted.append(i)

    return shortlisted


def check_free_rakes(arr):
    print("Checking free rakes")
    shortlisted = []
    for i in arr:
        if i["status"] == "free":
            shortlisted.append(i)

    return shortlisted


def min_distance(shortlisted_sources, shortlisted_rakes):
    while len(shortlisted_sources) > 0 and len(shortlisted_rakes) > 0:
        # time.sleep(1)
        minDist = 1000000
        source_id = -1
        rake_id = -1
        for i in shortlisted_rakes:
            for j in shortlisted_sources:
                consumer = j["consumer"]
                previousVal = minDist
                dist = distance(
                    i["location"][0],
                    i["location"][1],
                    j["location"][0],
                    j["location"][1],
                ) + distance(
                    j["location"][0],
                    j["location"][1],
                    consumers[consumer - 1]["location"][0],
                    consumers[consumer - 1]["location"][1],
                )
                print("{} is the distance from rake {} to source {} to consumer {}".format(dist, i["id"], j["id"], j["consumer"]))
                minDist = min(
                    dist,
                    minDist,
                )
                if minDist != previousVal:
                    source_id = j["id"]
                    rake_id = i["id"]

        values = {
            "id": rake_id,
            "status": "busy",
            "source": source_id,
            "distance": minDist,
        }
        change(rakes, sources, values)
        new_data = {
            "rakes": rakes,
            "sources": sources,
            "consumers": consumers,
            "rake_capacity": rake_capacity,
        }
        with open('sample.json', 'w') as wfile:
            json.dump(new_data, wfile)
        remover(shortlisted_rakes, rake_id)
        remover(shortlisted_sources, source_id)
        print(
            Fore.GREEN + "Rake {} will travel to source S{}".format(rake_id, source_id)
        )
        print(Style.RESET_ALL)


def change(rakes, sources, values):
    destination = -1
    for j in sources:
        if j["id"] == values["source"]:
            j["allocated"] = True
            destination = j["consumer"]
            j["stock"] -= rake_capacity
    for i in rakes:
        if i["id"] == values["id"]:
            i["status"] = values["status"]
            i["source"] = values["source"]
            i["destination"] = destination
            i["distance"] = values["distance"]


while True:
    free_sources = check_stock(sources, rake_capacity)
    free_rakes = check_free_rakes(rakes)
    print("Iterating")
    # print("Sources before {}".format(sources))
    min_distance(free_sources, free_rakes)
    # print("Sources after {}".format(sources))
    # for r in rakes:
    #     print(r["distance"])
    reducer(rakes)
    new_data = {
        "rakes": rakes,
        "sources": sources,
        "consumers": consumers,
        "rake_capacity": rake_capacity,
    }
    with open('sample.json', 'w') as wfile:
        json.dump(new_data, wfile)
    time.sleep(1)
    # for s in sources:
    #     if s["stock"] < 20:
    #         s["stock"] += 1
