import json

from flask import request

from Addons.Backend.Connection.UsersQuestionDAO import UsersQuestionDAO

UsersQuestionC = UsersQuestionDAO()


class UsersQuestionController:
    def create_users_question_controller(self):
        data = json.loads(request.data)
        new_data = []
        for i in data.values():
            new_data.append(i)
        return UsersQuestionC.create_user_question_dao(user=new_data[0], question=new_data[1], answer=new_data[2])

    def get_question_by_user_controller(self):
        data = json.loads(request.data)
        new_data = []
        for i in data.values():
            new_data.append(i)
        return UsersQuestionC.get_question_by_user_dao(user=new_data[0])

    def get_question_by_id_user_controller(self):
        data = json.loads(request.data)
        new_data = []
        for i in data.values():
            new_data.append(i)
        return UsersQuestionC.get_question_by_id_user_dao(id=new_data[0])

    def get_all_questions_by_user_controller(self):
        data = json.loads(request.data)
        new_data = []
        for i in data.values():
            new_data.append(i)
        return UsersQuestionC.get_all_questions_by_user_dao()
