class Locker:
    def __init__(self, locker_id, is_free):
        self.locker_id = locker_id
        self.is_free = is_free


class LockerService:
    def __init__(self):
        self.lockers = []

    # ----------- UserService connection logic -----------

    def __send_to_user_service(self, message):
        """ RabbitMQ logic for sending messages to UserService"""

    def __receive_from_user_service(self):
        """ RabbitMQ logic for receiving messages from UserService"""

    # ----------- DB logic -----------

    def __get_free_lockers(self, collection):
        """
        MongoDB logic for getting a list of free lockers
        collection.find({"is_free": True})
        returns list of locker ids (or empty list)
        """

    def __update_lockers_db(self, collection, locker_id, is_locked):
        """
        MongoDB logic to occupy or free a locker
        is_locked = True or False
        my_query = { locker_id: "$regex": "*" }
        new_value = { "$set": { "is_locked": is_locked } }
        collection.update_one(my_query, new_value)
        """

    def __occupy_locker(self, collection, locker_id):
        """ MongoDB logic for getting id of a free locker (if it exists)"""
        free_lockers = self.get_free_lockers()
        if len(free_lockers) > 0:
            return free_lockers[0]
            locker_id = free_lockers[0]
            # UPDATE locker table in db to lock a locker
            # use self.__update_lockers_db(collection, locker_id, True)
            return locker_id
        else:
            return -1

    # ----------- Service logic -----------

    def start(self):
        """ Start LockerService"""

    def stop(self):
        """ Stop LockerService"""
