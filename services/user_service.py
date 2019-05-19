class User:
    def __init__(self, user_id, name, locker_id=None):
        self.id = user_id
        self.name = name
        self.locker_id = locker_id


class UserService:
    def __init__(self):
        """ basic initializing """
        # TODO: self.users = [] ? think whether this is needed
        # TODO: self.cursor - some postgress

    # -----------------------------------------------
    # ----------- Locker connection logic -----------

    def __send_to_locker_service(self, message):
        """ Publisher rabbitqm logic of sending messages """

    def __receive_from_locker_service(self):
        """ Listener rabbitmq logic of receiving messages """

    # ----------- Locker connection logic -----------
    # -----------------------------------------------

    # --------------------------------
    # ----------- DB logic -----------

    def __connect_to_db(self):
        """ Connection to users_db logic """

    def __send_to_users_db(self, sql_query):
        """ 
        Send request to Postgres Users DB 
        receive answer from Users DB
        returns dict
        """
        " - request logic"
        " - parse logic "

        # TODO: decide to usu User class or dict
        user_locker_id_dict = dict(
            user_name="user_name_from_db",  #User.id
            locker_id="locker_id_from_db")  # = cursor.blabla
        return user_locker_id_dict

    def __receive_from_users_db(self, sql_query):
        """ Postgress logic on receiving messages from DB """
        # TODO: deside whether this function

    # ----------- DB logic -----------
    # --------------------------------

    def __add_user(self, name):
        """
        __send_to_users_db will be called
        """
        # TODO: change INSERT query
        sql_query = "INSERT query to add user to db"
        self.__send_to_users_db(sql_query)

    def __is_user_exists(self, dict):
        # TODO: discuss what DB will return in case of user not exists
        if (dict["user_name"] == None):
            return False
        else:
            return True

    def __is_locker_assigned(self, dict):
        # TODO: discuss what DB will return in case of locker_id empty
        if (dict["locker_id"] == None):
            return False
        else:
            return True

    # -------------------------------
    # ----------- FROM UI -----------

    def __on_check_button_clicked(self, name):
        """ make request to DB with name """

        # TODO: change SELECT query
        sql_query = "SELECT query to select user & its locker_id from table"
        user_locker_id_dict = self.__send_to_users_db(sql_query)

        if self.__is_user_exists:
            if self.__is_locker_assigned:
                self.__send_answer_to_ui(
                    self.__form_msg_to_ui("{0} - locker number: {1}".format(
                        user_locker_id_dict['user_name'],
                        user_locker_id_dict['locker_id'])))
            else:
                # TODO: discuss what message to send to locker to get locker_id
                self.__send_to_locker_service("Get locker_id")
                # TODO: deside how to receive locker_id (from which function)
                # TODO: __send_answer_to_ui send to UI user: locker_id
        else:
            self.__add_user(name)
            # TODO: discuss what message to send to locker to get locker_id
            self.__send_to_locker_service("Get locker_id")
            # TODO: deside how to receive locker_id (from which function)
            # TODO: __send_answer_to_ui user: locker_id

    # ----------- FROM UI -----------
    # -------------------------------

    # -----------------------------
    # ----------- TO UI -----------

    def __form_msg_to_ui(self, message, dict=None):
        """
        maybe will not be needed 
        concatenate message & dict 
        """
        #final_message = message + dict
        #return message

    def __send_answer_to_ui(self, message):
        """ send to ui logic """

    # ----------- TO UI -----------
    # -----------------------------

    def start(self):
        """ Start UserService """

    def stop(self):
        """ Stop UserService """
