import json

from flask import request

from Addons.Backend.Connection.UserDAO import UserDAO

UserC = UserDAO()


class UserController:
    def insert_user_controller(self, respose_json):
        data = respose_json["response"]
        parsed_data = {}
        for i in data:
            parsed_data = i
        return UserC.insert_user_dao(user=parsed_data.get("id"), avatar=parsed_data.get("photo_100"),
                                       name=parsed_data.get("first_name") + " " + parsed_data.get("last_name"))

    # def check_for_new_user_controller(self, response_json):
    #     data = json.loads(request.data)
    #     new_data = []
    #     for i in data.values():
    #         new_data.append(i)
    #     database = Database()
    #     result = User.insert_user_dao(username=new_data[0])
    #     return result

    def get_random_users_controller(self):
        data = json.loads(request.data)
        new_data = []
        for i in data.values():
            new_data.append(i)
        return UserC.get_random_users_dao(username=new_data[0])
