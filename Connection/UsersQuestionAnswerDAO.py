import json
import psycopg2
import os


class UsersQuestionAnswerDAO:
    def __init__(self):
        host_for_connection_str = os.environ.get(HOST)

        db_for_connection_str = os.environ.get(DATABASE)

        user_for_connection_str = os.environ.get(USER)

        port_for_connection_str = os.environ.get(PORT)

        password_for_connection_str = os.environ.get(PASSWORD)
        self.conn = psycopg2.connect(
            f"dbname={db_for_connection_str} user={user_for_connection_str} password={password_for_connection_str} host={host_for_connection_str} port={port_for_connection_str}")
        self.cur = self.conn.cursor()

    def insert_answer_to_users_question_dao(self, user, question, answer, date, creator):
        try:
            self.__init__()
            if answer == "":
                result = ["No"]
                return json.dumps(result)
            else:
                self.cur.execute(
                    '''SELECT (id) FROM public."USER" WHERE username='{}';'''.format(
                        creator)
                )
                creator_id_querry = self.cur.fetchone()
                for creator_id in creator_id_querry:
                    self.cur.execute(
                        '''SELECT (id) FROM public."USER" WHERE username='{}';'''.format(
                            user, )
                    )
                    row1 = self.cur.fetchone()
                    username_id = 0
                    for row in row1:
                        username_id = row

                    self.cur.execute(
                        '''SELECT (id) FROM public."USERSQUESTION" WHERE question='{}' AND user_id='{}';'''.format(
                            question, creator_id)
                    )
                    row2 = self.cur.fetchone()
                    question_id = 0
                    for row in row2:
                        question_id = row
                    self.cur.execute(
                        '''INSERT INTO public."USERS_QUESTION_ANSWER"(user_id, question_id, answer, date) VALUES('{}','{}','{}','{}')'''.format(
                            username_id, question_id, answer, date)
                    )
                    self.conn.commit()
                    return json.dumps(["Done"])
        finally:
            self.conn.close()

    def get_answers_on_users_question_dao(self, user):
        try:
            self.__init__()
            q_ids = []
            a_ids = []
            questions = []
            answers = []
            dates = []
            names = []
            avatars = []
            usernames = []
            result = []
            self.cur.execute(
                '''SELECT (id) FROM public."USER" WHERE username='{}';'''.format(
                    user, )
            )
            users = self.cur.fetchone()
            for user_id in users:

                self.cur.execute(
                    '''SELECT (question_id) FROM public."USERS_QUESTION_ANSWER" WHERE user_id='{}';'''.format(
                        user_id)
                )
                question_id_querry = self.cur.fetchall()
                for question_id_tuple in question_id_querry:
                    for question_id in question_id_tuple:
                        if question_id not in q_ids:
                            q_ids.append(question_id)
                for q_id in q_ids:
                    self.cur.execute(
                        '''SELECT id FROM public."USERS_QUESTION_ANSWER" WHERE user_id='{}' AND question_id='{}' ORDER BY date DESC FETCH FIRST ROW ONLY'''.format(
                            user_id, q_id)
                    )
                    last_id_answer = self.cur.fetchall()
                    for last_id_tuple in last_id_answer:
                        for last in last_id_tuple:
                            a_ids.append(last)
                    self.cur.execute(
                        '''SELECT answer FROM public."USERS_QUESTION_ANSWER" WHERE user_id='{}' AND question_id='{}' ORDER BY date DESC FETCH FIRST ROW ONLY'''.format(
                            user_id, q_id)
                    )
                    last_answer = self.cur.fetchall()
                    for last_tuple in last_answer:
                        for last in last_tuple:
                            answers.append(last)
                    self.cur.execute(
                        '''SELECT date FROM public."USERS_QUESTION_ANSWER" WHERE user_id='{}' AND question_id='{}' ORDER BY date DESC FETCH FIRST ROW ONLY'''.format(
                            user_id, q_id)
                    )
                    last_date = self.cur.fetchall()
                    for last_tuple in last_date:
                        for last in last_tuple:
                            dates.append(last)
                    self.cur.execute(
                        '''SELECT (question) FROM public."USERSQUESTION" WHERE id='{}';'''.format(
                            q_id)
                    )
                    question_querry = self.cur.fetchone()
                    for question in question_querry:
                        questions.append(question)
                    self.cur.execute(
                        '''SELECT (user_id) FROM public."USERSQUESTION" WHERE id='{}';'''.format(
                            q_id)
                    )
                    user_id_querry = self.cur.fetchone()
                    for user_idd in user_id_querry:
                        self.cur.execute(
                            '''SELECT (name) FROM public."USER" WHERE id='{}';'''.format(
                                user_idd)
                        )
                        name_querry = self.cur.fetchone()
                        for name in name_querry:
                            names.append(name)
                        self.cur.execute(
                            '''SELECT (avatar) FROM public."USER" WHERE id='{}';'''.format(
                                user_idd)
                        )
                        avatar_querry = self.cur.fetchone()
                        for avatar in avatar_querry:
                            avatars.append(avatar)
                        self.cur.execute(
                            '''SELECT (username) FROM public."USER" WHERE id='{}';'''.format(
                                user_idd)
                        )
                        username_querry = self.cur.fetchone()
                        for username in username_querry:
                            usernames.append(username)
            for question, answer, answerID, date, id, name, avatar, username in zip(questions, answers, a_ids, dates,
                                                                                    q_ids, names,
                                                                                    avatars, usernames):
                result.append(
                    {"id": id, "userUsername": username, "userName": name, "userAvatar": avatar, "question": question,
                     "answerID": answerID,
                     "answer": answer,
                     "date": str(date)})
            return json.dumps(result)
        finally:
            self.conn.close()

    def get_all_answers_on_users_question_dao(self, user, question, creator):
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
            self.cur.execute(
                '''SELECT (id) FROM public."USER" WHERE username='{}';'''.format(
                    creator, )
            )
            creator_ids = self.cur.fetchone()
            for iid, creator_id in zip(user_ids, creator_ids):
                self.cur.execute(
                    '''SELECT (id) FROM public."USERSQUESTION" WHERE question='{}' AND user_id='{}';'''.format(question,
                                                                                                               creator_id)
                )
                questions_id_querry = self.cur.fetchone()
                for question_id in questions_id_querry:
                    self.cur.execute(
                        '''SELECT (answer) FROM public."USERS_QUESTION_ANSWER" WHERE question_id='{}' AND user_id='{}';'''.format(
                            question_id, iid)
                    )
                    answer_querry = self.cur.fetchall()
                    for answer in answer_querry:
                        answers.append(answer)
                    self.cur.execute(
                        '''SELECT (date) FROM public."USERS_QUESTION_ANSWER" WHERE question_id='{}' AND user_id='{}';'''.format(
                            question_id, iid)
                    )
                    date_querry = self.cur.fetchall()
                    for date in date_querry:
                        dates.append(date)
                    self.cur.execute(
                        '''SELECT (id) FROM public."USERS_QUESTION_ANSWER" WHERE question_id='{}' AND user_id='{}';'''.format(
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

    def feed_dao(self, username):
        try:
            self.__init__()
            usernames = []
            avatars = []
            names = []
            questions = []
            questions_ids = []
            dates = []
            user_ids = []
            result = []
            self.cur.execute(
                '''SELECT (id) FROM public."USER" WHERE username='{}';'''.format(
                    username)
            )
            ids = self.cur.fetchone()
            for id in ids:
                self.cur.execute(
                    '''SELECT (question) FROM public."USERSQUESTION" WHERE NOT user_id='{}' AND isverified='{}';'''.format(
                        id, True)
                )
                questions_querry = self.cur.fetchall()
                for q_tuple in questions_querry:
                    for q in q_tuple:
                        questions.append(q)
                self.cur.execute(
                    '''SELECT (id) FROM public."USERSQUESTION" WHERE NOT user_id='{}' AND isverified='{}';'''.format(id,
                                                                                                                     True)
                )
                questions_id_querry = self.cur.fetchall()
                for q_tuple in questions_id_querry:
                    for q in q_tuple:
                        questions_ids.append(q)
                self.cur.execute(
                    '''SELECT (date) FROM public."USERSQUESTION"'''
                )
                date_querry = self.cur.fetchall()
                for d_tuple in date_querry:
                    for d in d_tuple:
                        dates.append(d)
                for q_id in questions_ids:
                    self.cur.execute(
                        '''SELECT user_id FROM public."USERSQUESTION" WHERE id='{}';'''.format(
                            q_id)
                    )
                    querry = self.cur.fetchone()
                    for u_id in querry:
                        user_ids.append(u_id)
                for user_id in user_ids:
                    self.cur.execute(
                        '''SELECT (username) FROM public."USER" WHERE id='{}';'''.format(
                            user_id)
                    )
                    username_querry = self.cur.fetchone()
                    for username in username_querry:
                        usernames.append(username)
                    self.cur.execute(
                        '''SELECT (avatar) FROM public."USER" WHERE id='{}';'''.format(
                            user_id)
                    )
                    avatar_querry = self.cur.fetchone()
                    for avatar in avatar_querry:
                        avatars.append(avatar)
                    self.cur.execute(
                        '''SELECT (name) FROM public."USER" WHERE id='{}';'''.format(
                            user_id)
                    )
                    name_querry = self.cur.fetchone()
                    for name in name_querry:
                        names.append(name)
            for i in range(len(questions)):
                result.append({"username": usernames[i], "name": names[i], "avatar": avatars[i],
                               "idOfQuestion": questions_ids[i], "question": questions[i],
                               "date": dates[i]})
            return json.dumps(result)
        finally:
            self.conn.close()

    def update_answer_on_users_dao(self, answerID, newAnswer):
        try:
            self.__init__()
            self.cur.execute(
                '''UPDATE public."USERS_QUESTION_ANSWER" SET answer='{}' WHERE id='{}';'''.format(
                    newAnswer, answerID)
            )
            self.conn.commit()
            return json.dumps(["Updated"])
        finally:
            self.conn.close()

    def delete_answer_users_dao(self, answerID):
        try:
            self.__init__()
            self.cur.execute(
                '''DELETE FROM public."USERS_QUESTION_ANSWER" WHERE id='{}';'''.format(
                    answerID)
            )
            self.conn.commit()
            return json.dumps(["Deleted"])
        finally:
            self.conn.close()
