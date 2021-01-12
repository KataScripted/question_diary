import json

from flask import request

from Addons.Backend.Controllers.UsersQuestionAnswerController import UsersQuestionAnswerController
from Addons.Backend.Services.VKApi import *

UsersQuestionAnswerControllerS = UsersQuestionAnswerController()


class UsersQuestionAnswerService:
    def __init__(self):
        self.secret = "khKzTP7LbxqTqIcXrcTq"

    def insert_answer_to_users_question_service(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            return UsersQuestionAnswerControllerS.insert_answer_to_users_question_controller()

    def get_answer_to_users_question_service(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            return UsersQuestionAnswerControllerS.get_answer_to_users_question_controller()

    def get_all_answers_to_users_question_service(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            return UsersQuestionAnswerControllerS.get_all_answers_to_users_question_controller()

    def feed_service(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            return UsersQuestionAnswerControllerS.feed_controller()

    def update_answer_user_service(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            return UsersQuestionAnswerControllerS.update_answer_on_users_controller()

    def delete_answer_user_service(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            return UsersQuestionAnswerControllerS.delete_answer_on_users_controller()
