if __name__ == "__main__":
    from pymongo import MongoClient
    client = MongoClient('localhost',
                        replicaSet='lockers_rs',
                        readPreference='secondaryPreferred')
    client.drop_database('lockers_db')
