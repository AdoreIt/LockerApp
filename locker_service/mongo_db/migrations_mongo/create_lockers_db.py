if __name__ == "__main__":
    from pymongo import MongoClient
    client = MongoClient('localhost')
    config = {'_id': 'lockers_rs', 'members': [
                {'_id': 0, 'host': 'localhost:27017'},
                {'_id': 1, 'host': 'localhost:27018'},
                {'_id': 2, 'host': 'localhost:27019'}]}
    client.admin.command("replSetInitiate", config)
    lockers_db = client["lockers_db"]
    lockers = lockers_db["lockers"]

    size = 20
    for i in range(size):
        lockers.insert_one({"_id": i, "free": True})

