from datetime import datetime
from pymongo import MongoClient


CONNECTION_STRING = 'mongodb://localhost:27017'


def __get_collection_name():
    date = datetime.now()
    return "urls_by_day_%d_%d_%d" % (date.day, date.month, date.year)


def ips_by_url(skip, limit):
    with MongoClient(CONNECTION_STRING) as client:
        pipeline = [
            {"$group": {"_id": "$Url", "Ips": {"$push": "$Ip"}}},
            {"$skip": skip},
            {"$limit": limit}
        ]
        result = client['Journal']['Visits'].aggregate(pipeline)
        return [(document["_id"], document["Ips"]) for document in result]


if __name__ == "__main__":
    for value in ips_by_url(0, 1000):
        print("%s:" % value[0])
        for ip in value[1]:
            print("     %s" % ip)
