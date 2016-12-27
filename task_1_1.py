import os
import pymongo

from datetime import datetime
from bson import Code
from pymongo import MongoClient

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONNECTION_STRING = 'mongodb://localhost:27017'


def __get_collection_name():
    date = datetime.now()
    return "ip_activity_report_%d_%d_%d" % (date.day, date.month, date.year)


def most_frequent_ips(skip, limit):
    with MongoClient(CONNECTION_STRING) as client:
        map_function = Code(
            open(os.path.join(BASE_DIR, r'DB_TEST\JavaScript\MostFrequentIpsMap.js')).read()
        )
        reduce_function = Code(
            open(os.path.join(BASE_DIR, r'DB_TEST\JavaScript\MostFrequentIpsReduce.js')).read()
        )
        result = client['Journal']['Visits'].map_reduce(map_function, reduce_function, __get_collection_name())
        return [(document['_id']['Ip'], document['value']['count'])
                for document in result.find().sort('value.count', pymongo.DESCENDING)[skip:limit]]


if __name__ == "__main__":
    for key, value in most_frequent_ips(0, 50):
        print("%-40s: %s" % (key, value))
