import time
from colorama import Fore, Style


def reducer(rakes):
    for r in rakes:
        if int(r["distance"]) == 0 and r["status"] == "busy":
            print("Rake {} has reached destination".format(r["id"]))
            sources[r["source"] - 1]["allocated"] = False
            r["status"] = "free"
            r["location"] = consumers[r["destination"] - 1]["location"]
            r["source"] = None
            r["destination"] = None

        if int(r["distance"]) > 0:
            r["distance"] -= 1
            print("Distance left for rake {}: {}".format(r["id"], int(r["distance"])))


def remover(arr, id):
    for i in arr:
        if i["id"] == id:
            arr.remove(i)


def distance(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


rakes = [
    {
        "id": 1,
        "status": "free",
        "source": None,
        "destination": None,
        "location": [4, 9],
        "distance": 0,
    },
    {
        "id": 2,
        "status": "free",
        "source": None,
        "destination": None,
        "location": [9, 21],
        "distance": 0,
    },
    {
        "id": 3,
        "status": "free",
        "source": None,
        "destination": None,
        "location": [8, 20],
        "distance": 0,
    },
]

rake_capacity = 10

sources = [
    {"id": 1, "stock": 30, "consumer": 1, "location": [10, 24], "allocated": False},
    {"id": 2, "stock": 11, "consumer": 2, "location": [-5, -22], "allocated": False},
    {"id": 3, "stock": 15, "consumer": 3, "location": [20, 3], "allocated": False},
    {"id": 4, "stock": 13, "consumer": 4, "location": [-13, 5], "allocated": False},
]

consumers = [
    {
        "id": 1,
        "stock": 5,
        "location": [-3, 20],
    },
    {
        "id": 2,
        "stock": 5,
        "location": [17, -15],
    },
    {
        "id": 3,
        "stock": 5,
        "location": [18, 27],
    },
    {
        "id": 4,
        "stock": 5,
        "location": [-11, 24],
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


# shortlisted_sources = check_stock(sources, rake_capacity)
# shortlisted_rakes = check_free_rakes(rakes)

# optimum_id = min_distance(shortlisted_sources, shortlisted_rakes)
# print("Rake {} will travel to source S{}".format(optimum_id[0], optimum_id[1]))

# shortlisted_sources = check_stock(sources, rake_capacity)
# shortlisted_rakes = check_free_rakes(rakes)
# next_optimum_id = min_distance(shortlisted_sources, shortlisted_rakes)
# print(
#     "Rake {} will travel to source S{}".format(next_optimum_id[0], next_optimum_id[1])
# )


while True:
    free_sources = check_stock(sources, rake_capacity)
    free_rakes = check_free_rakes(rakes)
    print("Iterating")
    # print("Sources before {}".format(sources))
    min_distance(free_sources, free_rakes)
    # print("Sources after {}".format(sources))
    # for r in rakes:
    #     print(r["distance"])
    print(rakes)
    reducer(rakes)
    time.sleep(1)
    # for s in sources:
    #     if s["stock"] < 20:
    #         s["stock"] += 1
