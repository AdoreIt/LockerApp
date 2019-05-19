class User:
    def __init__(self, user_id, name, locker_id=None):
        self.id = user_id
        self.name = name
        self.locker_id = locker_id


class UserService:
    def __init__(self):
        self.users = []

    # ----------- Locker connection logic -----------

    def __send_to_locker_service(self, message):
        """ rabbitqm logic of sending messages """

    def __receive_from_locker_service(self):
        """ rabbitmq logic of receiving messages """

    # ----------- Locker connection logic -----------

    # ----------- DB logic -----------

    def __send_to_users_db(self, sql_query):
        """ 
        Send request to Postgres Users DB 
        receive answer from Users DB
        returns dict
        """
        " - request logic"
        " - parse logic "

        user_locker_id_dict = dict(
            user="user_name_from_db",
            locker_id="locker_id_from_db")  # = cursor.blabla
        return user_locker_id_dict

    # def __receive_from_users_db(self, sql_query):
    #     """ Mongo logic on receiving messages from DB """

    # ----------- DB logic -----------

    # def __user_name(self):
    #     """
    #     Get unique user id from Mongo Users DB
    #     __send_to_users_db will be called
    #     """

    #     # SELECT query to check if

    def __is_user_exists(self, dict):
        # TODO: discuss what DB will return in case of user not exists
        if (dict["user"] == None):
            return False
        else:
            return True

    def __is_locker_assigned(self, dict):
        # TODO: discuss what DB will return in case of locker_id epmty
        if (dict["locker_id"] == None):
            return False
        else:
            return True

    # ----------- FROM UI -----------
    def __on_check_button_clicked(self, name):
        """ make request to DB with name """

        # TODO: change SELECT query
        sql_query = "SELECT query to select user & its locker_id from table"
        user_locker_id_dict = self.__send_to_users_db(sql_query)

        if self.__is_user_exists:
            if self.__is_locker_assigned:
                self.__send_answer_to_ui(
                    self.__form_msg_to_ui("message", user_locker_id_dict))

    # ----------- FROM UI -----------

    # ----------- TO UI -----------

    def __form_msg_to_ui(self, message, dict):
        """ concatenate message & dict """
        #final_message = message + dict
        #return message

    def __send_answer_to_ui(self, message):
        """ send to ui logic """

    # ----------- TO UI -----------
    def start(self):
        """ Start UserService """

    def stop(self):
        """ Stop UserService """
