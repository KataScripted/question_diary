import json

import requests
from flask import request

from Addons.Backend.Controllers.UserController import UserController
from Addons.Backend.Services.VKApi import *

UserControllerS = UserController()


class UserService:
    def __init__(self):
        self.secret = "khKzTP7LbxqTqIcXrcTq"

    def insert_user_service(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        userID = get_user_ID(query=headers, secret=self.secret)
        url = "https://api.vk.com/method/users.get?user_ids={}&fields=photo_100,&access_token=a435a2c3a435a2c3a435a2c30ea4474d11aa435a435a2c3fb31e24486d1299ee7e789b5&v=5.126".format(
            userID)
        print(url)
        r = requests.get(url=url)
        respose_json = r.json()
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            return UserControllerS.insert_user_controller(respose_json=respose_json)

    def get_random_users_service(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            return UserControllerS.get_random_users_controller()
