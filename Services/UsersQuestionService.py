import json

from flask import request

from Addons.Backend.Controllers.UsersQuestionController import UsersQuestionController
from Addons.Backend.Services.VKApi import *

UsersQuestionControllerS = UsersQuestionController()


class UsersQuestionService:
    def __init__(self):
        self.secret = "khKzTP7LbxqTqIcXrcTq"

    def create_users_question_service(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            return UsersQuestionControllerS.create_users_question_controller()

    def get_question_by_user_service(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            return UsersQuestionControllerS.get_question_by_user_controller()

    def get_question_by_id_user_service(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            return UsersQuestionControllerS.get_question_by_id_user_controller()

    def get_all_questions_by_user_service(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            return UsersQuestionControllerS.get_all_questions_by_user_controller()
