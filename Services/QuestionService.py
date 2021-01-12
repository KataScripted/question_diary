import json

from flask import request

from Addons.Backend.Controllers.QuestionController import QuestionController
from Addons.Backend.Services.VKApi import *

QuestionControllerS = QuestionController()


class QuestionService:
    def __init__(self):
        self.secret = "khKzTP7LbxqTqIcXrcTq"

    def get_answered_question_service(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            return QuestionControllerS.get_answered_question_controller()

    def get_all_questions_service(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            return QuestionControllerS.get_all_questions_controller()

    def get_new_question_service(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            return QuestionControllerS.get_new_question_controller()

    def get_question_by_id_admin_service(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            return QuestionControllerS.get_question_by_id_admin_controller()

    def get_question_by_category_service(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            return QuestionControllerS.get_question_by_category_controller()
