import time
from colorama import Fore, Style
import geopy.distance


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
            r["distance"] -= 1
            print("Distance left for rake {}: {}".format(r["id"], r["distance"]))


def remover(arr, id):
    for i in arr:
        if i["id"] == id:
            arr.remove(i)


def distance(x1, y1, x2, y2):
    return geopy.distance.geodesic([x1, y1], [x2, y2]).km

rakes = [
    {
        "id": 1,
        "status": "free",
        "source": None,
        "destination": None,
        "location": [19.769805,73.730762], # Nashik
        "distance": 0,
    },
    {
        "id": 2,
        "status": "free",
        "source": None,
        "destination": None,
        "location": [19.169037,73.115126], # Kalyan
        "distance": 0,
    },
    {
        "id": 3,
        "status": "free",
        "source": None,
        "destination": None,
        "location": [22.342963,75.399851], # Pithampur 
        "distance": 0,
    },
]

rake_capacity = 10

sources = [
    {"id": 1, "stock": 30, "consumer": 1, "location": [19.201333, 72.980793], "allocated": False}, # Mumbai
    {"id": 2, "stock": 11, "consumer": 2, "location": [22.680930,75.936453], "allocated": False}, # Indore
    {"id": 3, "stock": 15, "consumer": 3, "location": [16.831884,74.617003], "allocated": False}, # Sangli
    {"id": 4, "stock": 13, "consumer": 4, "location": [19.213653,77.343391], "allocated": False}, # Nanded
]

consumers = [
    {
        "id": 1,
        "stock": 5,
        "location": [18.485861,73.831224], # Pune
    },
    {
        "id": 2,
        "stock": 5,
        "location": [20.762278,75.304353], # Jalgaon
    },
    {
        "id": 3,
        "stock": 5,
        "location": [14.611226,74.820639], # Sirsi
    },
    {
        "id": 4,
        "stock": 5,
        "location": [17.377901,78.558429], # Hyderabad
    },
]


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
    time.sleep(1)
    # for s in sources:
    #     if s["stock"] < 20:
    #         s["stock"] += 1
