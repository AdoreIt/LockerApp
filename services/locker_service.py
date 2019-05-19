class Locker:
    def __init__(self, locker_id, is_free):
        self.locker_id = locker_ids
        self.is_free = is_free


class LockerService:
    def __init__(self):
        self.lockers = []

    def __send_to_user_service(self, message):
        """ RabbitMQ logic for sending messages to UserService"""

    def __receive_from_user_service(self):
        """ RabbitMQ logic for receiving messages from UserService"""

    def get_free_lockers(self):
        """ PostgreSQL logic for getting a list of free lockers"""

    def generate_free_locker(self):
        """ PostgreSQL logic for getting id of a free locker (if it exists)"""

    def start(self):
        """ Start LockerService"""
    
    def stop(self):
        """ Stop LockerService"""
