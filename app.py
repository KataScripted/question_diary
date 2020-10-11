import json
import psycopg2
from psycopg2.extras import NamedTupleCursor
from flask import Flask
from flask import request
from flask_cors import CORS
from config import user_for_connection_str, password_for_connection_str, host_for_connection_str, \
    port_for_connection_str, db_for_connection_str

app = Flask(__name__)
CORS(app)


class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            f"dbname={db_for_connection_str} user={user_for_connection_str} password={password_for_connection_str} host={host_for_connection_str} port={port_for_connection_str}")
        self.cur = self.conn.cursor()

    def insert_user(self, user, notification):
        try:
            self.cur.execute(

                '''SELECT username FROM public."USER" WHERE username='{}';'''.format(user, )
            )
            rows = self.cur.fetchall()
            if len(rows) > 0:
                self.conn.commit()
                result = ["Exists"]
                return json.dumps(result)
            else:
                self.cur.execute(
                    '''INSERT INTO public."USER"(username, notification) VALUES('{}','{}');'''.format(user,
                                                                                                      notification)
                )
                self.conn.commit()
                result = ["Inserted"]
                return json.dumps(result)

        finally:
            self.conn.close()

    def get_users_for_notification(self):
        try:
            self.cur.execute(
                '''SELECT (username) FROM public."USER" WHERE notification=True '''
            )
            users = self.cur.fetchall()
            new_users = []
            for users1 in users:
                for user in users1:
                    new_users.append(user)
            return json.dumps(new_users)
        finally:
            self.conn.close()

    def insert_answer(self, user, question, answer, date):
        try:
            if answer == "":
                result = ["No"]
                return json.dumps(result)
            else:
                self.cur.execute(
                    '''SELECT (id) FROM public."USER" WHERE username='{}';'''.format(user, )
                )
                row1 = self.cur.fetchone()
                username_id = 0
                for row in row1:
                    username_id = row

                self.cur.execute(
                    '''SELECT (id) FROM public."QUESTION" WHERE question='{}';'''.format(question, )
                )
                row2 = self.cur.fetchone()
                question_id = 0
                for row in row2:
                    question_id = row
                self.cur.execute(
                    '''INSERT INTO public."ANSWER"(user_id, question_id, answer, date) VALUES('{}','{}','{}','{}')'''.format(
                        username_id, question_id, answer, date)
                )
                self.conn.commit()
                result = ["Done"]
                return json.dumps(result)
        finally:
            self.conn.close()

    def get_answer_by_date(self, user, date):
        try:
            answers_d = {}
            questions = []
            question_text = []
            self.cur.execute(
                '''SELECT (id) FROM public."USER" WHERE username='{}';'''.format(user, )
            )
            users = self.cur.fetchone()
            for user_id in users:
                self.cur.execute(
                    '''SELECT (question_id) FROM public."ANSWER" WHERE user_id='{}' AND date='{}';'''.format(user_id,
                                                                                                             date)
                )
            questions_guery = self.cur.fetchall()
            for q in questions_guery:
                for qq in q:
                    questions.append(qq)
            print(questions)
            for user_id in users:
                self.cur.execute(
                    '''SELECT (answer) FROM public."ANSWER" WHERE user_id='{}' AND date='{}';'''.format(user_id,
                                                                                                             date)
                )
            answers = self.cur.fetchall()
            for q_id in questions:
                self.cur.execute(
                    '''SELECT (question) FROM public."QUESTION" WHERE id='{}';'''.format(q_id, )
                )
                questions_text = self.cur.fetchall()
                for q in questions_text:
                    question_text.append(q)

            for question_tuple, answer_tuple in zip(question_text, answers):
                print(question_tuple)
                print(answer_tuple)
                for question1, answer1 in zip(question_tuple, answer_tuple):
                    answers_d.update({question1: answer1})
            print(answers_d)
            return json.dumps(answers_d)
        finally:
            self.conn.close()

    def get_answered_questions(self, user):
        try:
            self.cur.execute(
                '''SELECT (id) FROM public."USER" WHERE username='{}';'''.format(user, )
            )
            users = self.cur.fetchone()
            for user_id in users:
                self.cur.execute(
                    '''SELECT (question_id) FROM public."ANSWER" WHERE user_id='{}';'''.format(user_id, )
                )
            questions = []
            answers = []
            answers_d = {}
            questions_ids = self.cur.fetchall()
            for question_id in questions_ids:
                for id in question_id:
                    self.cur.execute(
                        '''SELECT (question) FROM public."QUESTION" WHERE id='{}';'''.format(id, )
                    )
                    id_of_question = self.cur.fetchone()
                    questions.append(id_of_question)
            for user_id in users:
                self.cur.execute(
                    '''SELECT (answer) FROM public."ANSWER" WHERE user_id='{}';'''.format(user_id)
                )
                answers1 = self.cur.fetchall()
                for answer1 in answers1:
                    answers.append(answer1)
            for question_tuple, answer_tuple in zip(questions, answers):
                for question1, answer1 in zip(question_tuple, answer_tuple):
                    answers_d.update({question1: answer1})
            return json.dumps(answers_d)
        finally:
            self.conn.close()

    def get_all_questions(self):
        try:
            self.cur.execute(
                '''SELECT * FROM public."QUESTION"'''
            )
            rows = self.cur.fetchall()
            return json.dumps(rows)
        finally:
            self.conn.close()

    def get_new_question(self, user):
        try:
            all_questions = []
            questions = []
            result_list = []
            last_list_result = []
            self.cur.execute(
                '''SELECT (question) FROM public."QUESTION"'''
            )
            rows = self.cur.fetchall()
            for row in rows:
                for r in row:
                    all_questions.append(r)
            self.cur.execute(
                '''SELECT (id) FROM public."USER" WHERE username='{}';'''.format(user, )
            )
            user_ids = self.cur.fetchone()
            for user_id in user_ids:
                self.cur.execute(
                    '''SELECT (question_id) FROM public."ANSWER" WHERE user_id='{}';'''.format(user_id, )
                )
                question_ids = self.cur.fetchall()
                for question_id in question_ids:
                    for q in question_id:
                        self.cur.execute(
                            '''SELECT (question) FROM public."QUESTION" WHERE id='{}';'''.format(q, )
                        )
                        ques = self.cur.fetchall()
                        for q in ques:
                            for q1 in q:
                                questions.append(q1)
            for question in all_questions:
                if question in questions:
                    pass
                else:
                    result_list.append(question)

            last_list_result.append(result_list[0])
            return json.dumps(last_list_result)
        finally:
            self.conn.close()
    
    def get_all_answers_on_question(self,user,question):
        try:
            cur = self.conn.cursor(cursor_factory=NamedTupleCursor)
            result = []
            self.cur.execute(
                '''SELECT (id) FROM public."USER" WHERE username='{}';'''.format(user, )
            )
            user_ids = self.cur.fetchone()
            for iid in user_ids:
                self.cur.execute(
                    '''SELECT (question_id) FROM public."ANSWER" WHERE user_id='{}';'''.format(iid, )
                )
                question_ids = self.cur.fetchall()
                for question_id in question_ids:
                    for q_id in question_id:
                        cur.execute(
                            '''SELECT (question_id, answer, date) FROM public."ANSWER" WHERE question_id='{}';'''.format(q_id,)
                        )
                        answer_querry = cur.fetchall()
            return json.dumps(answer_querry)
        finally:
            self.conn.close()

@app.route('/insertuser', methods=["GET", "POST"])
def insert_user():
    data = json.loads(request.data)
    new_data = []
    for i in data.values():
        new_data.append(i)
    database = Database()
    result = database.insert_user(user=new_data[0], notification=new_data[1])
    return result


@app.route('/insertanswer', methods=["GET", "POST"])
def insert_answer1():
    data = json.loads(request.data)
    new_data = []
    for i in data.values():
        new_data.append(i)
    database = Database()
    result = database.insert_answer(user=new_data[0], question=new_data[1], answer=new_data[2], date=new_data[3])
    return result


@app.route('/questions', methods=["GET"])
def get_all_questions():
    database = Database()
    result = database.get_all_questions()
    return result


@app.route('/answered', methods=["GET", "POST"])
def answered():
    data = json.loads(request.data)
    new_data = []
    for i in data.values():
        new_data.append(i)
    database = Database()
    result = database.get_answered_questions(user=new_data[0])
    return result


@app.route('/notification', methods=["GET"])
def get_users_for_notification():
    database = Database()
    result = database.get_users_for_notification()
    return result


@app.route('/questionbydate', methods=["GET", "POST"])
def get_question_by_date():
    data = json.loads(request.data)
    new_data = []
    for i in data.values():
        new_data.append(i)
    database = Database()
    result = database.get_answer_by_date(user=new_data[0], date=new_data[1])
    return result


@app.route('/newquestion', methods=["GET", "POST"])
def get_new_question():
    data = json.loads(request.data)
    new_data = []
    for i in data.values():
        new_data.append(i)
    database = Database()
    result = database.get_new_question(user=new_data[0])
    return result


@app.route('/allanswers', methods=["GET", "POST"])
def get_all_answers_on_question():
    data = json.loads(request.data)
    new_data = []
    for i in data.values():
        new_data.append(i)
    database = Database()
    result = database.get_all_answers_on_question(user=new_data[0],question=new_data[1])
    return result


if __name__ == '__main__':
    app.run(debug=True)