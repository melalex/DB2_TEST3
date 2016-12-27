from bson import SON
from pymongo import MongoClient

CONNECTION_STRING = 'mongodb://localhost:27017'


def urls_by_day(skip, limit):
    with MongoClient(CONNECTION_STRING) as client:
        pipeline = [
            {"$group": {"_id": {"VisitDate": "$VisitDate", "Url": "$Url"}, "count": {"$sum": 1}}},
            {"$sort": SON([("count", -1), ("_id", -1)])},
            {"$skip": skip},
            {"$limit": limit}
        ]
        result = client['Journal']['Visits'].aggregate(pipeline)
        return [(document["_id"]["VisitDate"], document["_id"]["Url"], document["count"]) for document in result]


if __name__ == "__main__":
    for value in urls_by_day(0, 1000):
        print("%s | %-100s | %s" % (value[0], value[1], value[2]))
