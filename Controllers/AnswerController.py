import json

from flask import request

from Addons.Backend.Connection.AnswerDAO import AnswerDAO

AnswerC = AnswerDAO()


class AnswerController:
    def insert_answer_controller(self):
        data = json.loads(request.data)
        new_data = []
        for i in data.values():
            new_data.append(i)
        return AnswerC.insert_answer_dao(user=new_data[0], question=new_data[1], answer=new_data[2], date=new_data[3])

    def get_answer_by_date_contoller(self):
        data = json.loads(request.data)
        new_data = []
        for i in data.values():
            new_data.append(i)
        return AnswerC.get_answer_by_date_dao(user=new_data[0], date=new_data[1])

    def get_all_answers_on_question_controller(self):
        data = json.loads(request.data)
        new_data = []
        for i in data.values():
            new_data.append(i)
        return AnswerC.get_all_answers_on_question_dao(user=new_data[0], question=new_data[1])

    def update_answer_controller(self):
        data = json.loads(request.data)
        new_data = []
        for i in data.values():
            new_data.append(i)
        return AnswerC.update_answer_dao(answerID=new_data[0], newAnswer=new_data[1])

    def delete_answer_controller(self):
        data = json.loads(request.data)
        new_data = []
        for i in data.values():
            new_data.append(i)
        return AnswerC.delete_answer_dao(answerID=new_data[0])
