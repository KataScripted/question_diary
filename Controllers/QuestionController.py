import json

from flask import request

from Addons.Backend.Connection.QuestionDAO import QuestionDAO

QuestionC = QuestionDAO()


class QuestionController:
    def get_answered_question_controller(self):
        data = json.loads(request.data)
        new_data = []
        for i in data.values():
            new_data.append(i)
        return QuestionC.get_answered_questions_dao(user=new_data[0])

    def get_all_questions_controller(self):
        return QuestionC.get_all_questions_dao()

    def get_new_question_controller(self):
        data = json.loads(request.data)
        new_data = []
        for i in data.values():
            new_data.append(i)
        return QuestionC.get_new_question_dao(user=new_data[0])

    def get_question_by_id_admin_controller(self):
        data = json.loads(request.data)
        new_data = []
        for i in data.values():
            new_data.append(i)
        return QuestionC.get_question_by_id_admin_dao(id=new_data[0])

    def get_question_by_category_controller(self):
        data = json.loads(request.data)
        new_data = []
        for i in data.values():
            new_data.append(i)
        return QuestionC.get_questions_by_category_dao(user=new_data[0],category=new_data[1])
