import json
import psycopg2
import os


class AnswerDAO:
    def __init__(self):
        host_for_connection_str = os.environ.get(HOST)

        db_for_connection_str = os.environ.get(DATABASE)

        user_for_connection_str = os.environ.get(USER)

        port_for_connection_str = os.environ.get(PORT)

        password_for_connection_str = os.environ.get(PASSWORD)
        self.conn = psycopg2.connect(
            f"dbname={db_for_connection_str} user={user_for_connection_str} password={password_for_connection_str} host={host_for_connection_str} port={port_for_connection_str}")
        self.cur = self.conn.cursor()

    def insert_answer_dao(self, user, question, answer, date):
        try:
            self.__init__()
            if answer == "":
                result = ["No"]
                return json.dumps(result)
            else:
                self.cur.execute(
                    '''SELECT (id) FROM public."USER" WHERE username='{}';'''.format(
                        user, )
                )
                row1 = self.cur.fetchone()
                username_id = 0
                for row in row1:
                    username_id = row

                self.cur.execute(
                    '''SELECT (id) FROM public."QUESTION" WHERE question='{}';'''.format(
                        question, )
                )
                row2 = self.cur.fetchone()
                question_id = 0
                for row in row2:
                    question_id = row
                self.cur.execute(
                    '''INSERT INTO public."ANSWER"(user_id, question_id, answer, datee) VALUES('{}','{}','{}','{}')'''.format(
                        username_id, question_id, answer, date)
                )
                self.conn.commit()
                result = ["Done"]
                return json.dumps(result)
        finally:
            self.conn.close()

    def get_answer_by_date_dao(self, user, date):
        try:
            self.__init__()
            answers_d = []
            questions = []
            question_text = []
            self.cur.execute(
                '''SELECT (id) FROM public."USER" WHERE username='{}';'''.format(
                    user, )
            )
            users = self.cur.fetchone()
            for user_id in users:
                self.cur.execute(
                    '''SELECT (question_id) FROM public."ANSWER" WHERE user_id='{}' AND datee='{}';'''.format(user_id,
                                                                                                              date)
                )
            questions_guery = self.cur.fetchall()
            for q in questions_guery:
                for qq in q:
                    questions.append(qq)
            for user_id in users:
                self.cur.execute(
                    '''SELECT (answer) FROM public."ANSWER" WHERE user_id='{}' AND datee='{}';'''.format(user_id,
                                                                                                         date)
                )
            answers = self.cur.fetchall()
            for user_id in users:
                self.cur.execute(
                    '''SELECT (id) FROM public."ANSWER" WHERE user_id='{}' AND datee='{}';'''.format(user_id,
                                                                                                     date)
                )
            answer_ids = self.cur.fetchall()
            for q_id in questions:
                self.cur.execute(
                    '''SELECT (question) FROM public."QUESTION" WHERE id='{}';'''.format(
                        q_id, )
                )
                questions_text = self.cur.fetchall()
                for q in questions_text:
                    question_text.append(q)
            for question_tuple, answer_tuple, id, answer_id_tuple in zip(question_text, answers, questions, answer_ids):
                for question1, answer1, answerID in zip(question_tuple, answer_tuple, answer_id_tuple):
                    answers_d.append(
                        {"id": id, "question": question1, "answerID": answerID, "answer": answer1})
            if bool(answers_d):
                return json.dumps(answers_d)
            else:
                return json.dumps(["No"])
        finally:
            self.conn.close()

    def get_all_answers_on_question_dao(self, user, question):
        try:
            self.__init__()
            result_d = []
            answers = []
            dates = []
            ids = []
            self.cur.execute(
                '''SELECT (id) FROM public."USER" WHERE username='{}';'''.format(
                    user, )
            )
            user_ids = self.cur.fetchone()
            for iid in user_ids:
                self.cur.execute(
                    '''SELECT (id) FROM public."QUESTION" WHERE question='{}';'''.format(
                        question, )
                )
                question_ids = self.cur.fetchone()
                for question_id in question_ids:

                    self.cur.execute(
                        '''SELECT (answer) FROM public."ANSWER" WHERE question_id='{}' AND user_id='{}';'''.format(
                            question_id, iid)
                    )
                    answer_querry = self.cur.fetchall()
                    for answer in answer_querry:
                        answers.append(answer)
                    self.cur.execute(
                        '''SELECT (datee) FROM public."ANSWER" WHERE question_id='{}' AND user_id='{}';'''.format(
                            question_id, iid)
                    )
                    date_querry = self.cur.fetchall()
                    for date in date_querry:
                        dates.append(date)
                    self.cur.execute(
                        '''SELECT (id) FROM public."ANSWER" WHERE question_id='{}' AND user_id='{}';'''.format(
                            question_id, iid)
                    )
                    id_querry = self.cur.fetchall()
                    for id in id_querry:
                        ids.append(id)
            for date_tuple, answer_tuple, id_tuple in zip(dates, answers, ids):
                for date1, answer1, id in zip(date_tuple, answer_tuple, id_tuple):
                    result_d.append(
                        {"answerID": id, "answer": answer1, "date": str(date1)})
            return json.dumps(result_d)
        finally:
            self.conn.close()

    def update_answer_dao(self, answerID, newAnswer):
        try:
            self.__init__()
            self.cur.execute(
                '''UPDATE public."ANSWER" SET answer='{}' WHERE id='{}';'''.format(
                    newAnswer, answerID)
            )
            self.conn.commit()
            return json.dumps(["Updated"])
        finally:
            self.conn.close()

    def delete_answer_dao(self, answerID):
        try:
            self.__init__()
            self.cur.execute(
                '''DELETE FROM public."ANSWER" WHERE id='{}';'''.format(
                    answerID)
            )
            self.conn.commit()
            return json.dumps(["Deleted"])
        finally:
            self.conn.close()
