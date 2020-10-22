import json

from flask import request

from Connection.Database import Database



class Controller:
    def __init__(self):
        pass

    def insert_user(self):
        data = json.loads(request.data)
        new_data = []
        for i in data.values():
            new_data.append(i)
        database = Database()
        result = database.insert_user(user=new_data[0], notification=new_data[1], avatar=new_data[2], name=new_data[3])
        return result

    def insert_answer(self):
        data = json.loads(request.data)
        new_data = []
        for i in data.values():
            new_data.append(i)
        database = Database()
        result = database.insert_answer(user=new_data[0], question=new_data[1], answer=new_data[2], date=new_data[3])
        return result

    def get_all_questions(self):
        database = Database()
        result = database.get_all_questions()
        return result

    def answered(self):
        data = json.loads(request.data)
        new_data = []
        for i in data.values():
            new_data.append(i)
        database = Database()
        result = database.get_answered_questions(user=new_data[0])
        return result

    def get_users_for_notification(self):
        database = Database()
        result = database.get_users_for_notification()
        return result

    def get_question_by_date(self):
        data = json.loads(request.data)
        new_data = []
        for i in data.values():
            new_data.append(i)
        database = Database()
        result = database.get_answer_by_date(user=new_data[0], date=new_data[1])
        return result

    def get_new_question(self):
        data = json.loads(request.data)
        new_data = []
        for i in data.values():
            new_data.append(i)
        database = Database()
        result = database.get_new_question(user=new_data[0])
        return result

    def get_all_answers_on_question(self):
        data = json.loads(request.data)
        new_data = []
        for i in data.values():
            new_data.append(i)
        database = Database()
        result = database.get_all_answers_on_question(user=new_data[0], question=new_data[1])
        return result

    def create_question(self):
        data = json.loads(request.data)
        new_data = []
        for i in data.values():
            new_data.append(i)
        database = Database()
        result = database.create_user_question(user=new_data[0], question=new_data[1])
        return result

    def insert_answer_to_users_question(self):
        data = json.loads(request.data)
        new_data = []
        for i in data.values():
            new_data.append(i)
        database = Database()
        result = database.insert_answer_to_users_question(user=new_data[0], question=new_data[1], answer=new_data[2],
                                                          date=new_data[3])
        return result

    def question_by_user(self):
        data = json.loads(request.data)
        new_data = []
        for i in data.values():
            new_data.append(i)
        database = Database()
        result = database.get_question_by_user(user=new_data[0])
        return result

    def answered_on_users_question(self):
        data = json.loads(request.data)
        new_data = []
        for i in data.values():
            new_data.append(i)
        database = Database()
        result = database.get_answers_on_users_question(user=new_data[0])
        return result

    def get_users_with_most_answered(self):
        database = Database()
        result = database.get_user_with_most_answered_questions()
        return result
