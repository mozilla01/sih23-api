def distance(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


rakes = [
    {
        "id": 1,
        "status": "free",
        "source": None,
        "destination": None,
        "location": [4, 9],
    },
    {
        "id": 2,
        "status": "free",
        "source": None,
        "destination": None,
        "location": [5, 10],
    },
    {
        "id": 3,
        "status": "free",
        "source": None,
        "destination": None,
        "location": [-4, -21],
    },
]

rake_capacity = 10

sources = [
    {"id": 1, "stock": 20, "consumer": 1, "location": [10, 24], "allocated": False},
    {"id": 2, "stock": 11, "consumer": 2, "location": [-5, -22], "allocated": False},
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
]


def check_stock(arr, capacity):
    shortlisted = []
    for i in arr:
        if i["stock"] >= capacity and i["allocated"] == False:
            shortlisted.append(i)

    return shortlisted


def check_free_rakes(arr):
    shortlisted = []
    for i in arr:
        if i["status"] == "free":
            shortlisted.append(i)

    return shortlisted


def min_distance(shortlisted_sources, rakes):
    print("Calculating min distance")
    minDist = 1000000
    source_id = -1
    rake_id = -1
    for i in rakes:
        print("Distances")
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
            print(dist)
            minDist = min(
                dist,
                minDist,
            )
            if minDist != previousVal:
                source_id = j["id"]
                rake_id = i["id"]

    rakes[rake_id - 1]["status"] = "busy"
    rakes[rake_id - 1]["source"] = source_id
    sources[source_id - 1]["allocated"] = True
    destination = sources[source_id - 1]["consumer"]
    rakes[rake_id - 1]["destination"] = consumers[destination - 1]["id"]

    return [rake_id, source_id]


shortlisted_sources = check_stock(sources, rake_capacity)
shortlisted_rakes = check_free_rakes(rakes)

optimum_id = min_distance(shortlisted_sources, shortlisted_rakes)
print("Rake {} will travel to source S{}".format(optimum_id[0], optimum_id[1]))

shortlisted_sources = check_stock(sources, rake_capacity)
shortlisted_rakes = check_free_rakes(rakes)
next_optimum_id = min_distance(shortlisted_sources, shortlisted_rakes)
print(
    "Rake {} will travel to source S{}".format(next_optimum_id[0], next_optimum_id[1])
)
