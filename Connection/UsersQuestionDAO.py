import json
import datetime
import psycopg2
import os


class UsersQuestionDAO:
    def __init__(self):
        host_for_connection_str = os.environ.get(HOST)

        db_for_connection_str = os.environ.get(DATABASE)

        user_for_connection_str = os.environ.get(USER)

        port_for_connection_str = os.environ.get(PORT)

        password_for_connection_str = os.environ.get(PASSWORD)
        self.conn = psycopg2.connect(
            f"dbname={db_for_connection_str} user={user_for_connection_str} password={password_for_connection_str} host={host_for_connection_str} port={port_for_connection_str}")
        self.cur = self.conn.cursor()

    def create_user_question_dao(self, user, question, answer):
        try:
            self.__init__()
            date = datetime.datetime.now().date()
            self.cur.execute(
                '''SELECT (id) FROM public."USER" WHERE username='{}';'''.format(
                    user, )
            )
            user_id_querry = self.cur.fetchone()
            for user_id in user_id_querry:
                self.cur.execute(
                    '''SELECT (id) FROM public."USERSQUESTION" WHERE user_id='{}' AND question='{}';'''.format(user_id,
                                                                                                               question)
                )
                exists = self.cur.fetchall()
                if exists != []:
                    return json.dumps(["Dublicate"])
                else:
                    self.cur.execute(
                        '''INSERT INTO public."USERSQUESTION"(question, user_id, date) VALUES('{}','{}','{}');'''.format(
                            question,
                            user_id, date)
                    )
                    self.conn.commit()
                    self.cur.execute(
                        '''SELECT (id) FROM public."USERSQUESTION" WHERE question='{}';'''.format(
                            question)
                    )
                    question_id_quarry = self.cur.fetchone()
                    if answer == "":
                        return json.dumps(["Created"])
                    else:
                        for question_id in question_id_quarry:
                            self.cur.execute(
                                '''INSERT INTO public."USERS_QUESTION_ANSWER"(user_id, question_id, answer, date) VALUES('{}','{}','{}','{}')'''.format(
                                    user_id, question_id, answer, date))
                        self.conn.commit()
            return json.dumps(["Created"])
        finally:
            self.conn.close()

    def get_question_by_user_dao(self, user):
        try:
            self.__init__()
            result = []
            self.cur.execute(
                '''SELECT (id) FROM public."USER" WHERE username='{}';'''.format(
                    user, )
            )
            user_id_querry = self.cur.fetchone()
            for user_id in user_id_querry:
                self.cur.execute(
                    '''SELECT (question) FROM public."USERSQUESTION" WHERE user_id='{}';'''.format(
                        user_id, )
                )
                question_querry = self.cur.fetchall()
                self.cur.execute(
                    '''SELECT (id) FROM public."USERSQUESTION" WHERE user_id='{}';'''.format(
                        user_id, )
                )
                ids_querry = self.cur.fetchall()
                if len(question_querry) == 0:
                    return json.dumps(["No questions"])
                self.cur.execute(
                    '''SELECT (date) FROM public."USERSQUESTION" WHERE user_id='{}';'''.format(
                        user_id, )
                )
                date_querry = self.cur.fetchall()
                for id_tuple, question_tuple, date_tuple in zip(ids_querry, question_querry, date_querry):
                    for id, question, date in zip(id_tuple, question_tuple, date_tuple):
                        result.append(
                            {"id": id, "question": question, "date": str(date)})
            return json.dumps(result)
        finally:
            self.conn.close()

    def get_question_by_id_user_dao(self, id):
        try:
            self.__init__()
            result = []
            creators = []
            self.cur.execute(
                '''SELECT (question) FROM public."USERSQUESTION" WHERE id='{}';'''.format(
                    id)
            )
            q_querry = self.cur.fetchone()
            self.cur.execute(
                '''SELECT (user_id) FROM public."USERSQUESTION" WHERE id='{}';'''.format(
                    id)
            )
            c_querry = self.cur.fetchone()
            for c_id in c_querry:
                self.cur.execute(
                    '''SELECT (username) FROM public."USER" WHERE id='{}';'''.format(
                        c_id)
                )
                creator_querry = self.cur.fetchone()
                for i in creator_querry:
                    creators.append(i)
            for question, creator in zip(q_querry, creators):
                result.append({"question": question, "creator": creator})
            return json.dumps(result)
        finally:
            self.conn.close()

    def get_all_questions_by_user_dao(self):
        try:
            self.__init__()
            result = []
            questions = []
            ids = []
            self.cur.execute(
                '''SELECT (question) FROM public."USERSQUESTION"'''
            )
            querry = self.cur.fetchall()
            for question_tuple in querry:
                for question in question_tuple:
                    questions.append(question)

            self.cur.execute(
                '''SELECT (id) FROM public."USERSQUESTION"'''
            )
            querry = self.cur.fetchall()
            for id_tuple in querry:
                for id in id_tuple:
                    ids.append(id)
            for id, q in zip(ids, questions):
                result.append({"id": id, "question": q})
            return json.dumps(result)
        finally:
            self.conn.close()
