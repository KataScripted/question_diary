import json

from base64 import b64encode
from collections import OrderedDict
from hashlib import sha256
from hmac import HMAC
from urllib.parse import urlparse, parse_qsl, urlencode

from Connection.Database import Database
from flask import request


class Controller:
    def __init__(self):
        pass

    secret = "khKzTP7LbxqTqIcXrcTq"

    def is_valid(self, query: dict, secret: str) -> bool:
        """Check VK Apps signature"""
        vk_subset = filter(
            lambda key: key.startswith("vk_"),
            query
        )
        ordered = {k: query[k] for k in sorted(vk_subset)}
        hash_code = b64encode(
            HMAC(
                secret.encode(),
                urlencode(ordered, doseq=True).encode(),
                sha256
            ).digest()
        ).decode("utf-8")
        fixed_hash = hash_code[:-1 if hash_code[-1] == "=" else None].replace('+', '-').replace('/', '_')
        return query.get("sign") == fixed_hash

    def insert_user(self):
        url = request.url
        query_params = dict(parse_qsl(urlparse(url).query, keep_blank_values=True))
        access = self.is_valid(query=query_params, secret=self.secret)
        if access:
            data = json.loads(request.data)
            new_data = []
            for i in data.values():
                new_data.append(i)
            database = Database()
            result = database.insert_user_dao(user=new_data[0], avatar=new_data[1],
                                              name=new_data[2])
            return result
        else:
            return json.dumps(["Access Denied"])

    def check_for_new_user(self):
        q = request.args.items()
        print(q)
        query_params = dict(parse_qsl(urlparse(url).query, keep_blank_values=True))
        print(query_params)
        access = self.is_valid(query=query_params, secret=self.secret)
        if access:
            data = json.loads(request.data)
            new_data = []
            for i in data.values():
                new_data.append(i)
            database = Database()
            result = database.check_for_new_user_dao(username=new_data[0])
            return result
        else:
            return json.dumps(["Access Denied"])

    def insert_answer(self):
        url = request.url

        query_params = dict(parse_qsl(urlparse(url).query, keep_blank_values=True))
        access = self.is_valid(query=query_params, secret=self.secret)
        if access:
            data = json.loads(request.data)
            new_data = []
            for i in data.values():
                new_data.append(i)
            database = Database()
            result = database.insert_answer_dao(user=new_data[0], question=new_data[1], answer=new_data[2],
                                                date=new_data[3])
            return result
        else:
            return json.dumps(["Access Deniec"])

    def get_all_questions(self):
        url = request.url
        query_params = dict(parse_qsl(urlparse(url).query, keep_blank_values=True))
        access = self.is_valid(query=query_params, secret=self.secret)
        if access:
            database = Database()
            result = database.get_all_questions_dao()
            return result
        else:
            return json.dumps(["Access Denied"])

    def answered(self):
        url = request.url
        query_params = dict(parse_qsl(urlparse(url).query, keep_blank_values=True))
        access = self.is_valid(query=query_params, secret=self.secret)
        if access:
            data = json.loads(request.data)
            new_data = []
            for i in data.values():
                new_data.append(i)
            database = Database()
            result = database.get_answered_questions_dao(user=new_data[0])
            return result
        else:
            return json.dumps(["Access Denied"])

    # def get_users_for_notification(self):
    #     database = Database()
    #     result = database.get_users_for_notification_dao()
    #     return result

    def get_question_by_date(self):
        url = request.url
        query_params = dict(parse_qsl(urlparse(url).query, keep_blank_values=True))
        access = self.is_valid(query=query_params, secret=self.secret)
        if access:
            data = json.loads(request.data)
            new_data = []
            for i in data.values():
                new_data.append(i)
            database = Database()
            result = database.get_answer_by_date_dao(user=new_data[0], date=new_data[1])
            return result
        else:
            return json.dumps(["Access Denied"])

    def get_new_question(self):
        url = request.url
        query_params = dict(parse_qsl(urlparse(url).query, keep_blank_values=True))
        access = self.is_valid(query=query_params, secret=self.secret)
        if access:
            data = json.loads(request.data)
            new_data = []
            for i in data.values():
                new_data.append(i)
            database = Database()
            result = database.get_new_question_dao(user=new_data[0])
            return result
        else:
            return json.dumps(["Access Denied"])

    def get_all_answers_on_question(self):
        url = request.url
        query_params = dict(parse_qsl(urlparse(url).query, keep_blank_values=True))
        access = self.is_valid(query=query_params, secret=self.secret)
        if access:
            data = json.loads(request.data)
            new_data = []
            for i in data.values():
                new_data.append(i)
            database = Database()
            result = database.get_all_answers_on_question_dao(user=new_data[0], question=new_data[1])
            return result
        else:
            return json.dumps(["Access Denied"])

    def create_question(self):
        url = request.url
        query_params = dict(parse_qsl(urlparse(url).query, keep_blank_values=True))
        access = self.is_valid(query=query_params, secret=self.secret)
        if access:
            data = json.loads(request.data)
            new_data = []
            for i in data.values():
                new_data.append(i)
            database = Database()
            result = database.create_user_question_dao(user=new_data[0], question=new_data[1], answer=new_data[2])
            return result
        else:
            return json.dumps(["Access Denied"])

    def insert_answer_to_users_question(self):
        url = request.url
        query_params = dict(parse_qsl(urlparse(url).query, keep_blank_values=True))
        access = self.is_valid(query=query_params, secret=self.secret)
        if access:
            data = json.loads(request.data)
            new_data = []
            for i in data.values():
                new_data.append(i)
            database = Database()
            result = database.insert_answer_to_users_question_dao(user=new_data[0], question=new_data[1],
                                                                  answer=new_data[2],
                                                                  date=new_data[3],
                                                                  creator=new_data[4])
            return result
        else:
            return json.dumps(["Access Denied"])

    def question_by_user(self):
        url = request.url
        query_params = dict(parse_qsl(urlparse(url).query, keep_blank_values=True))
        access = self.is_valid(query=query_params, secret=self.secret)
        if access:
            data = json.loads(request.data)
            new_data = []
            for i in data.values():
                new_data.append(i)
            database = Database()
            result = database.get_question_by_user_dao(user=new_data[0])
            return result
        else:
            return json.dumps(["Access Denied"])

    def answered_on_users_question(self):
        url = request.url
        query_params = dict(parse_qsl(urlparse(url).query, keep_blank_values=True))
        access = self.is_valid(query=query_params, secret=self.secret)
        if access:
            data = json.loads(request.data)
            new_data = []
            for i in data.values():
                new_data.append(i)
            database = Database()
            result = database.get_answers_on_users_question_dao(user=new_data[0])
            return result
        else:
            return json.dumps(["Access Denied"])

    def get_all_answers_on_users_question(self):
        url = request.url
        query_params = dict(parse_qsl(urlparse(url).query, keep_blank_values=True))
        access = self.is_valid(query=query_params, secret=self.secret)
        if access:
            data = json.loads(request.data)
            new_data = []
            for i in data.values():
                new_data.append(i)
            database = Database()
            result = database.get_all_answers_on_users_question_dao(user=new_data[0], question=new_data[1],
                                                                    creator=new_data[2])
            return result
        else:
            return json.dumps(["Access Denied"])

    # def get_users_with_most_answered(self):
    #     database = Database()
    #     result = database.get_user_with_most_answered_questions_dao()
    #     return result
    #
    # def dayly_mood(self):
    #     data = json.loads(request.data)
    #     new_data = []
    #     for i in data.values():
    #         new_data.append(i)
    #     database = Database()
    #     result = database.set_dayly_mood_dao(user=new_data[0], mood=new_data[1], date=new_data[2])
    #     return result
    #
    # def get_mood_report(self):
    #     data = json.loads(request.data)
    #     new_data = []
    #     for i in data.values():
    #         new_data.append(i)
    #     database = Database()
    #     result = database.get_mood_report_dao(user=new_data[0])
    #     return result

    def get_question_by_id_admin(self):
        url = request.url
        query_params = dict(parse_qsl(urlparse(url).query, keep_blank_values=True))
        access = self.is_valid(query=query_params, secret=self.secret)
        if access:
            data = json.loads(request.data)
            new_data = []
            for i in data.values():
                new_data.append(i)
            database = Database()
            result = database.get_question_by_id_admin_dao(id=new_data[0])
            return result
        else:
            return json.dumps(["Access Denied"])

    def get_question_by_id_user(self):
        url = request.url
        query_params = dict(parse_qsl(urlparse(url).query, keep_blank_values=True))
        access = self.is_valid(query=query_params, secret=self.secret)
        if access:
            data = json.loads(request.data)
            new_data = []
            for i in data.values():
                new_data.append(i)
            database = Database()
            result = database.get_question_by_id_user_dao(id=new_data[0])
            return result
        else:
            return json.dumps(["Access Denied"])

    def all_question_by_users(self):
        url = request.url
        query_params = dict(parse_qsl(urlparse(url).query, keep_blank_values=True))
        access = self.is_valid(query=query_params, secret=self.secret)
        if access:
            database = Database()
            result = database.all_questions_by_user_dao()
            return result
        else:
            return json.dumps(["Access Denied"])

    def get_user_info(self):
        url = request.url
        query_params = dict(parse_qsl(urlparse(url).query, keep_blank_values=True))
        access = self.is_valid(query=query_params, secret=self.secret)
        if access:
            data = json.loads(request.data)
            new_data = []
            for i in data.values():
                new_data.append(i)
            database = Database()
            result = database.get_random_users_dao(username=new_data[0])
            return result
        else:
            return json.dumps(["Access Denied"])

    def feed(self):
        url = request.url
        query_params = dict(parse_qsl(urlparse(url).query, keep_blank_values=True))
        access = self.is_valid(query=query_params, secret=self.secret)
        if access:
            data = json.loads(request.data)
            new_data = []
            for i in data.values():
                new_data.append(i)
            database = Database()
            result = database.feed_dao(username=new_data[0])
            return result
        else:
            return json.dumps(["Access Denied"])

    def get_question_by_category(self):
        url = request.url
        query_params = dict(parse_qsl(urlparse(url).query, keep_blank_values=True))
        access = self.is_valid(query=query_params, secret=self.secret)
        if access:
            data = json.loads(request.data)
            new_data = []
            for i in data.values():
                new_data.append(i)
            database = Database()
            result = database.get_questions_by_category_dao(user=new_data[0], category=new_data[1])
            return result
        else:
            return json.dumps(["Access Denied"])

    def update_answer(self):
        url = request.url
        query_params = dict(parse_qsl(urlparse(url).query, keep_blank_values=True))
        access = self.is_valid(query=query_params, secret=self.secret)
        if access:
            data = json.loads(request.data)
            new_data = []
            for i in data.values():
                new_data.append(i)
            database = Database()
            result = database.update_answer_dao(answerID=new_data[0], newAnswer=new_data[1])
            return result
        else:
            return json.dumps(["Access Denied"])

    def update_answer_user(self):
        url = request.url
        query_params = dict(parse_qsl(urlparse(url).query, keep_blank_values=True))
        access = self.is_valid(query=query_params, secret=self.secret)
        if access:
            data = json.loads(request.data)
            new_data = []
            for i in data.values():
                new_data.append(i)
            database = Database()
            result = database.update_answer_on_users_dao(answerID=new_data[0], newAnswer=new_data[1])
            return result
        else:
            return json.dumps(["Access Denied"])

    def delete_answer(self):
        url = request.url
        query_params = dict(parse_qsl(urlparse(url).query, keep_blank_values=True))
        access = self.is_valid(query=query_params, secret=self.secret)
        if access:
            data = json.loads(request.data)
            new_data = []
            for i in data.values():
                new_data.append(i)
            database = Database()
            result = database.delete_answer_dao(answerID=new_data[0])
            return result
        else:
            return json.dumps(["Access Denied"])

    def delete_answer_users(self):
        url = request.url
        query_params = dict(parse_qsl(urlparse(url).query, keep_blank_values=True))
        access = self.is_valid(query=query_params, secret=self.secret)
        if access:
            data = json.loads(request.data)
            new_data = []
            for i in data.values():
                new_data.append(i)
            database = Database()
            result = database.delete_answer_users_dao(answerID=new_data[0])
            return result
        else:
            return json.dumps(["Access Denied"])

    def complaint(self):
        url = request.url
        query_params = dict(parse_qsl(urlparse(url).query, keep_blank_values=True))
        access = self.is_valid(query=query_params, secret=self.secret)
        if access:
            data = json.loads(request.data)
            new_data = []
            for i in data.values():
                new_data.append(i)
            database = Database()
            result = database.complaint_dao(username=new_data[0], question_id=new_data[1], text=new_data[2])
            return result
        else:
            json.dumps(["Access Denied"])
