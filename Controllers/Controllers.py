import json
import requests
from base64 import b64encode
from hashlib import sha256
from hmac import HMAC
from urllib.parse import urlencode


from Connection.Database import Database
from flask import request



def is_valid(query: dict, secret: str) -> bool:
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

def get_user_ID(query: dict, secret: str) -> bool:
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
    return query.get("vk_user_id")


class Controller:
    def __init__(self):
        pass

    secret = "khKzTP7LbxqTqIcXrcTq"

    def insert_user(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        userID = get_user_ID(query=headers, secret=self.secret)
        url = "https://api.vk.com/method/users.get?user_ids={}&fields=photo_100,&access_token=a435a2c3a435a2c3a435a2c30ea4474d11aa435a435a2c3fb31e24486d1299ee7e789b5&v=5.126".format(userID)
        print(url)
        r = requests.get(url=url)
        respose_json = r.json()
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            data = respose_json["response"]
            parsed_data = {}
            for i in data:
                parsed_data = i
            database = Database()
            result = database.insert_user_dao(user=parsed_data.get("id"), avatar=parsed_data.get("photo_100"),
                                              name=parsed_data.get("first_name")+" "+parsed_data.get("last_name"))
            return result

    def check_for_new_user(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            data = json.loads(request.data)
            new_data = []
            for i in data.values():
                new_data.append(i)
            database = Database()
            result = database.check_for_new_user_dao(username=new_data[0])
            return result

    def insert_answer(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            data = json.loads(request.data)
            new_data = []
            for i in data.values():
                new_data.append(i)
            database = Database()
            result = database.insert_answer_dao(user=new_data[0], question=new_data[1], answer=new_data[2],
                                                date=new_data[3])
            return result

    def get_all_questions(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            database = Database()
            result = database.get_all_questions_dao()
            return result

    def answered(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            data = json.loads(request.data)
            new_data = []
            for i in data.values():
                new_data.append(i)
            database = Database()
            result = database.get_answered_questions_dao(user=new_data[0])
            return result

    # def get_users_for_notification(self):
    #     database = Database()
    #     result = database.get_users_for_notification_dao()
    #     return result

    def get_question_by_date(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            data = json.loads(request.data)
            new_data = []
            for i in data.values():
                new_data.append(i)
            database = Database()
            result = database.get_answer_by_date_dao(user=new_data[0], date=new_data[1])
            return result

    def get_new_question(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            data = json.loads(request.data)
            new_data = []
            for i in data.values():
                new_data.append(i)
            database = Database()
            result = database.get_new_question_dao(user=new_data[0])
            return result

    def get_all_answers_on_question(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            data = json.loads(request.data)
            new_data = []
            for i in data.values():
                new_data.append(i)
            database = Database()
            result = database.get_all_answers_on_question_dao(user=new_data[0], question=new_data[1])
            return result

    def create_question(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            data = json.loads(request.data)
            new_data = []
            for i in data.values():
                new_data.append(i)
            database = Database()
            result = database.create_user_question_dao(user=new_data[0], question=new_data[1], answer=new_data[2])
            return result

    def insert_answer_to_users_question(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
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

    def question_by_user(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            data = json.loads(request.data)
            new_data = []
            for i in data.values():
                new_data.append(i)
            database = Database()
            result = database.get_question_by_user_dao(user=new_data[0])
            return result

    def answered_on_users_question(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            data = json.loads(request.data)
            new_data = []
            for i in data.values():
                new_data.append(i)
            database = Database()
            result = database.get_answers_on_users_question_dao(user=new_data[0])
            return result

    def get_all_answers_on_users_question(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            data = json.loads(request.data)
            new_data = []
            for i in data.values():
                new_data.append(i)
            database = Database()
            result = database.get_all_answers_on_users_question_dao(user=new_data[0], question=new_data[1],
                                                                    creator=new_data[2])
            return result

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
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            data = json.loads(request.data)
            new_data = []
            for i in data.values():
                new_data.append(i)
            database = Database()
            result = database.get_question_by_id_admin_dao(id=new_data[0])
            return result

    def get_question_by_id_user(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            data = json.loads(request.data)
            new_data = []
            for i in data.values():
                new_data.append(i)
            database = Database()
            result = database.get_question_by_id_user_dao(id=new_data[0])
            return result

    def all_question_by_users(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            database = Database()
            result = database.all_questions_by_user_dao()
            return result

    def get_user_info(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            data = json.loads(request.data)
            new_data = []
            for i in data.values():
                new_data.append(i)
            database = Database()
            result = database.get_random_users_dao(username=new_data[0])
            return result

    def feed(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            data = json.loads(request.data)
            new_data = []
            for i in data.values():
                new_data.append(i)
            database = Database()
            result = database.feed_dao(username=new_data[0])
            return result

    def get_question_by_category(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            data = json.loads(request.data)
            new_data = []
            for i in data.values():
                new_data.append(i)
            database = Database()
            result = database.get_questions_by_category_dao(user=new_data[0], category=new_data[1])
            return result

    def update_answer(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            data = json.loads(request.data)
            new_data = []
            for i in data.values():
                new_data.append(i)
            database = Database()
            result = database.update_answer_dao(answerID=new_data[0], newAnswer=new_data[1])
            return result

    def update_answer_user(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            data = json.loads(request.data)
            new_data = []
            for i in data.values():
                new_data.append(i)
            database = Database()
            result = database.update_answer_on_users_dao(answerID=new_data[0], newAnswer=new_data[1])
            return result

    def delete_answer(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            data = json.loads(request.data)
            new_data = []
            for i in data.values():
                new_data.append(i)
            database = Database()
            result = database.delete_answer_dao(answerID=new_data[0])
            return result

    def delete_answer_users(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            data = json.loads(request.data)
            new_data = []
            for i in data.values():
                new_data.append(i)
            database = Database()
            result = database.delete_answer_users_dao(answerID=new_data[0])
            return result

    def complaint(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            data = json.loads(request.data)
            new_data = []
            for i in data.values():
                new_data.append(i)
            database = Database()
            result = database.complaint_dao(username=new_data[0], question_id=new_data[1], text=new_data[2])
            return result
