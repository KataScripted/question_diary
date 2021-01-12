import json

from flask import request

from Addons.Backend.Controllers.AnswerController import AnswerController
from Addons.Backend.Services.VKApi import *

AnswerControllerS = AnswerController()


class AnswerService:
    def __init__(self):
        self.secret = "khKzTP7LbxqTqIcXrcTq"

    def insert_answer_service(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            return AnswerControllerS.insert_answer_controller()

    def get_answer_answer_by_date_service(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            return AnswerControllerS.get_answer_by_date_contoller()

    def get_all_answers_on_question_service(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            return AnswerControllerS.get_all_answers_on_question_controller()

    def update_answer_service(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            return AnswerControllerS.update_answer_controller()

    def delete_answer_service(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            return AnswerControllerS.delete_answer_controller()
