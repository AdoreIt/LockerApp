if __name__ == "__main__":
    from pymongo import MongoClient
    client = MongoClient('localhost', replicaset='lockers_rs')
    config = {'_id': 'lockers_rs', 'members': [
                {'_id': 0, 'host': 'localhost:27017'},
                {'_id': 1, 'host': 'localhost:27018'},
                {'_id': 2, 'host': 'localhost:27019'}]}
    lockers_db = client["lockers_db"]
    lockers = lockers_db["lockers"]

    size = 21
    for i in range(1, size):
        lockers.insert_one({"_id": i, "free": True})

    print(lockers)
