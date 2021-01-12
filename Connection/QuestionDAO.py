import json
import psycopg2
import os 


class QuestionDAO:
    def __init__(self):
        host_for_connection_str = os.environ.get(HOST)

        db_for_connection_str = os.environ.get(DATABASE)

        user_for_connection_str = os.environ.get(USER)

        port_for_connection_str = os.environ.get(PORT)

        password_for_connection_str = os.environ.get(PASSWORD)
        self.conn = psycopg2.connect(
            f"dbname={db_for_connection_str} user={user_for_connection_str} password={password_for_connection_str} host={host_for_connection_str} port={port_for_connection_str}")
        self.cur = self.conn.cursor()

    def get_answered_questions_dao(self, user):
        try:
            self.__init__()
            q_ids = []
            a_ids = []
            questions = []
            answers = []
            dates = []
            result = []
            self.cur.execute(
                '''SELECT (id) FROM public."USER" WHERE username='{}';'''.format(user, )
            )
            users = self.cur.fetchone()
            for user_id in users:

                self.cur.execute(
                    '''SELECT (question_id) FROM public."ANSWER" WHERE user_id='{}' ORDER BY id DESC;'''.format(user_id)
                )
                question_id_querry = self.cur.fetchall()
                for question_id_tuple in question_id_querry:
                    for question_id in question_id_tuple:
                        if question_id not in q_ids:
                            q_ids.append(question_id)
                for q_id in q_ids:
                    self.cur.execute(
                        '''SELECT id FROM public."ANSWER" WHERE user_id='{}' AND question_id='{}' ORDER BY datee DESC FETCH FIRST ROW ONLY'''.format(
                            user_id, q_id)
                    )
                    last_id_answer = self.cur.fetchall()
                    for last_id_tuple in last_id_answer:
                        for last in last_id_tuple:
                            a_ids.append(last)
                    self.cur.execute(
                        '''SELECT answer FROM public."ANSWER" WHERE user_id='{}' AND question_id='{}' ORDER BY datee DESC FETCH FIRST ROW ONLY'''.format(
                            user_id, q_id)
                    )
                    last_answer = self.cur.fetchall()
                    for last_tuple in last_answer:
                        for last in last_tuple:
                            answers.append(last)
                    self.cur.execute(
                        '''SELECT datee FROM public."ANSWER" WHERE user_id='{}' AND question_id='{}' ORDER BY datee DESC FETCH FIRST ROW ONLY'''.format(
                            user_id, q_id)
                    )
                    last_date = self.cur.fetchall()
                    for last_tuple in last_date:
                        for last in last_tuple:
                            dates.append(last)
                    self.cur.execute(
                        '''SELECT (question) FROM public."QUESTION" WHERE id='{}';'''.format(q_id)
                    )
                    question_querry = self.cur.fetchone()
                    for question in question_querry:
                        questions.append(question)
            for question, answer, date, id, answerID in zip(questions, answers, dates, q_ids, a_ids):
                result.append(
                    {"id": id, "question": question, "answerID": answerID, "answer": answer, "date": str(date)})
            return json.dumps(result)
        finally:
            self.conn.close()

    def get_all_questions_dao(self):
        try:
            self.__init__()
            result = []
            self.cur.execute(
                '''SELECT * FROM public."QUESTION"'''
            )
            rows = self.cur.fetchall()
            for row in rows:
                result.append({"id": row[0], "question": row[1]})
            return json.dumps(result)
        finally:
            self.conn.close()

    def get_new_question_dao(self, user):
        try:
            self.__init__()
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

    def get_question_by_id_admin_dao(self, id):
        try:
            self.__init__()
            result = []
            self.cur.execute(
                '''SELECT (question) FROM public."QUESTION" WHERE id='{}';'''.format(id)
            )
            q_querry = self.cur.fetchone()
            for question in q_querry:
                result.append({"question": question})
            return json.dumps(result)
        finally:
            self.conn.close()

    def get_questions_by_category_dao(self, user, category):
        try:
            self.__init__()
            id_answered_questions = []
            answered_questions = []
            answers = []
            id_answers = []
            date_answered = []
            questions = []
            ids = []
            result = []
            self.cur.execute(
                '''SELECT (question) FROM public."QUESTION" WHERE category='{}';'''.format(category)
            )
            questions_question = self.cur.fetchall()
            for question_tuple in questions_question:
                for question in question_tuple:
                    questions.append(question)
            self.cur.execute(
                '''SELECT (id) FROM public."QUESTION" WHERE category='{}';'''.format(category)
            )
            ids_question = self.cur.fetchall()
            for id_tuple in ids_question:
                for id in id_tuple:
                    ids.append(id)

            self.cur.execute(
                '''SELECT (id) FROM public."USER" WHERE username='{}';'''.format(user)
            )
            user_id_querry = self.cur.fetchone()
            for user_id in user_id_querry:
                for id_q in ids:
                    self.cur.execute(
                        '''SELECT (question_id) FROM public."ANSWER" WHERE user_id='{}' AND question_id='{}';'''.format(
                            user_id, id_q)
                    )
                    id_anwered_querry = self.cur.fetchone()
                    if id_anwered_querry != None:
                        for id_answered_q in id_anwered_querry:
                            id_answered_questions.append(id_answered_q)
                            self.cur.execute(
                                '''SELECT (question) FROM public."QUESTION" WHERE id='{}';'''.format(id_answered_q)
                            )
                            question_answered_querry = self.cur.fetchone()
                            for q in question_answered_querry:
                                answered_questions.append(q)
                    self.cur.execute(
                        '''SELECT (datee) FROM public."ANSWER" WHERE user_id='{}' AND question_id='{}';'''.format(
                            user_id, id_q)
                    )
                    date_anwered_querry = self.cur.fetchone()
                    if date_anwered_querry != None:
                        for dt in date_anwered_querry:
                            date_answered.append(dt)
                    self.cur.execute(
                        '''SELECT (answer) FROM public."ANSWER" WHERE user_id='{}' AND question_id='{}';'''.format(
                            user_id, id_q)
                    )
                    answer_anwered_querry = self.cur.fetchone()
                    if answer_anwered_querry != None:
                        for a in answer_anwered_querry:
                            answers.append(a)
                    self.cur.execute(
                        '''SELECT (id) FROM public."ANSWER" WHERE user_id='{}' AND question_id='{}';'''.format(
                            user_id, id_q)
                    )
                    id_of_answers_querry = self.cur.fetchone()
                    if id_of_answers_querry != None:
                        for a in id_of_answers_querry:
                            id_answers.append(a)

            for item in id_answered_questions:
                ids.remove(item)
            for item in answered_questions:
                questions.remove(item)

            for id, question, answer, date, answerID in zip(id_answered_questions, answered_questions, answers,
                                                            date_answered, id_answers):
                result.append(
                    {"id": id, "question": question, "isAnswered": True, "answerID": answerID, "answer": answer,
                     "date": str(date)})
            for id, question in zip(ids, questions):
                result.append({"id": id, "question": question, "isAnswered": False})
            return json.dumps(result)
        finally:
            self.conn.close()
