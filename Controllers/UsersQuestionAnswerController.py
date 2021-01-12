import json

from flask import request

from Addons.Backend.Connection.UsersQuestionAnswerDAO import UsersQuestionAnswerDAO

UsersQuestionAnswerC = UsersQuestionAnswerDAO()


class UsersQuestionAnswerController:
    def insert_answer_to_users_question_controller(self):
        data = json.loads(request.data)
        new_data = []
        for i in data.values():
            new_data.append(i)
        return UsersQuestionAnswerC.insert_answer_to_users_question_dao(user=new_data[0], question=new_data[1], answer=new_data[2], date=new_data[3], creator=new_data[4])

    def get_answer_to_users_question_controller(self):
        data = json.loads(request.data)
        new_data = []
        for i in data.values():
            new_data.append(i)
        return UsersQuestionAnswerC.get_answers_on_users_question_dao(user=new_data[0])

    def get_all_answers_to_users_question_controller(self):
        data = json.loads(request.data)
        new_data = []
        for i in data.values():
            new_data.append(i)
        return UsersQuestionAnswerC.get_all_answers_on_users_question_dao(user=new_data[0], question=new_data[1], creator=new_data[2])

    def feed_controller(self):
        data = json.loads(request.data)
        new_data = []
        for i in data.values():
            new_data.append(i)
        return UsersQuestionAnswerC.feed_dao(username=new_data[0])

    def update_answer_on_users_controller(self):
        data = json.loads(request.data)
        new_data = []
        for i in data.values():
            new_data.append(i)
        return UsersQuestionAnswerC.update_answer_on_users_dao(answerID=new_data[0], newAnswer=new_data[1])

    def delete_answer_on_users_controller(self):
        data = json.loads(request.data)
        new_data = []
        for i in data.values():
            new_data.append(i)
        return UsersQuestionAnswerC.delete_answer_users_dao(answerID=new_data[0])
