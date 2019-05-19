class User:
    def __init__(self, user_id, name, locker_id=None):
        self.id = user_id
        self.name = name
        self.locker_id = locker_id


class UserService:
    def __init__(self):
        self.users = []

    def __send_to_locker_service(self, message):
        """ rabbitqm logic of sending messages """

    def __receive_from_locker_service(self):
        """ rabbitmq logic of receiving messages """

    def __send_to_users_db(self):
        """ Send request to Mongo Users DB """

    def __receive_from_users_db(self):
        """ Mongo logic on receiving messages from DB """

    def __generate_user_id(self):
        """
        Get uniq user id from Mongo Users DB 
        __send_to_users_db will be called
        """

    def start(self):
        """ Start UserService """

    def stop(self):
        """ Stop UserService """
