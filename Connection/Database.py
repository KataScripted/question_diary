import json
import random
import psycopg2


class Database:
    def __init__(self):
        host_for_connection_str = "ec2-34-232-212-164.compute-1.amazonaws.com"

        db_for_connection_str = "dda36o54of7pm6"

        user_for_connection_str = "zcvpawmwciwjix"

        port_for_connection_str = "5432"

        password_for_connection_str = "906fca382d57a5254ffec5ad08d47820d815e041bc8c4ba1f5386e26f54f3b68"
        self.conn = psycopg2.connect(
            f"dbname={db_for_connection_str} user={user_for_connection_str} password={password_for_connection_str} host={host_for_connection_str} port={port_for_connection_str}")
        self.cur = self.conn.cursor()

    def insert_user_dao(self, user, notification, avatar, name):
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
                    '''INSERT INTO public."USER"(username, notification, avatar, name) VALUES('{}','{}','{}','{}');'''.format(
                        user,
                        notification, avatar, name)
                )
                self.conn.commit()
                result = ["Inserted"]
                return json.dumps(result)

        finally:
            self.conn.close()

    def get_users_for_notification_dao(self):
        try:
            result = []
            self.cur.execute(
                '''SELECT (username) FROM public."USER" WHERE notification=True'''
            )
            users = self.cur.fetchall()
            self.cur.execute(
                '''SELECT (id) FROM public."USER" WHERE notification=True'''
            )
            ids = self.cur.fetchall()
            new_users = []
            for users1 in users:
                for user in users1:
                    new_users.append(user)
            new_ids = []
            for ids1 in ids:
                for id in ids1:
                    new_ids.append(id)
            for id, username in zip(new_ids, new_users):
                result.append({"id": id, "username": username})
            return json.dumps(result)
        finally:
            self.conn.close()

    def insert_answer_dao(self, user, question, answer, date):
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
            answers_d = []
            questions = []
            question_text = []
            self.cur.execute(
                '''SELECT (id) FROM public."USER" WHERE username='{}';'''.format(user, )
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
            for q_id in questions:
                self.cur.execute(
                    '''SELECT (question) FROM public."QUESTION" WHERE id='{}';'''.format(q_id, )
                )
                questions_text = self.cur.fetchall()
                for q in questions_text:
                    question_text.append(q)
            length = len(question_text)
            for question_tuple, answer_tuple, id in zip(question_text, answers, range(length)):
                for question1, answer1 in zip(question_tuple, answer_tuple):
                    answers_d.append({"id": id, "question": question1, "answer": answer1})
            if bool(answers_d):
                return json.dumps(answers_d)
            else:
                return json.dumps(["No"])
        finally:
            self.conn.close()

    def get_answered_questions_dao(self, user):
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
            dates = []
            answers_d = []
            questions_ids = self.cur.fetchall()
            for question_id in questions_ids:
                for id in question_id:
                    self.cur.execute(
                        '''SELECT (question) FROM public."QUESTION" WHERE id='{}';'''.format(id, )
                    )
                    question = self.cur.fetchone()
                    questions.append(question)

            for user_id in users:
                self.cur.execute(
                    '''SELECT (answer) FROM public."ANSWER" WHERE user_id='{}';'''.format(user_id)
                )
                answers1 = self.cur.fetchall()
                for answer1 in answers1:
                    answers.append(answer1)
                self.cur.execute(
                    '''SELECT (datee) FROM public."ANSWER" WHERE user_id='{}';'''.format(user_id)
                )
                dates1 = self.cur.fetchall()
                for date1 in dates1:
                    dates.append(date1)
                for question_tuple, answer_tuple, id_tuple, dates_tuple in zip(questions, answers, questions_ids,
                                                                               dates):
                    for question1, answer1, id, date in zip(question_tuple, answer_tuple, id_tuple, dates_tuple):
                        answers_d.append({"id": id, "question": question1, "answer": answer1, "date": str(date)})
            return json.dumps(answers_d)
        finally:
            self.conn.close()

    def get_all_questions_dao(self):
        try:
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

    def get_all_answers_on_question_dao(self, user, question):
        try:
            result_d = []
            answers = []
            dates = []
            self.cur.execute(
                '''SELECT (id) FROM public."USER" WHERE username='{}';'''.format(user, )
            )
            user_ids = self.cur.fetchone()
            for iid in user_ids:
                self.cur.execute(
                    '''SELECT (id) FROM public."QUESTION" WHERE question='{}';'''.format(question, )
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
            length = len(dates)
            for date_tuple, answer_tuple, id in zip(dates, answers, range(length)):
                for date1, answer1 in zip(date_tuple, answer_tuple):
                    result_d.append({"id": id, "answer": answer1, "date": str(date1)})
            return json.dumps(result_d)
        finally:
            self.conn.close()

    def create_user_question_dao(self, user, question):
        try:
            self.cur.execute(
                '''SELECT (id) FROM public."USER" WHERE username='{}';'''.format(user, )
            )
            user_id_querry = self.cur.fetchone()
            for user_id in user_id_querry:
                self.cur.execute(
                    '''INSERT INTO public."USERSQUESTION"(question, user_id) VALUES('{}','{}');'''.format(question,
                                                                                                          user_id)
                )
                self.conn.commit()
            return json.dumps(["Created"])
        finally:
            self.conn.close()

    def insert_answer_to_users_question_dao(self, user, question, answer, date):
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
                    '''SELECT (id) FROM public."USERSQUESTION" WHERE question='{}';'''.format(question, )
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

    def get_question_by_user_dao(self, user):
        try:
            result = []
            self.cur.execute(
                '''SELECT (id) FROM public."USER" WHERE username='{}';'''.format(user, )
            )
            user_id_querry = self.cur.fetchone()
            if user_id_querry == None:
                return json.dumps(["No questions"])
            else:
                for user_id in user_id_querry:
                    self.cur.execute(
                        '''SELECT (question) FROM public."USERSQUESTION" WHERE user_id='{}';'''.format(user_id, )
                    )
                    question_querry = self.cur.fetchall()
                for question_tuple in question_querry:
                    for question in question_tuple:
                        result.append({"question": question})
                return json.dumps(result)
        finally:
            self.conn.close()

    def get_answers_on_users_question_dao(self, user):
        try:
            self.cur.execute(
                '''SELECT (id) FROM public."USER" WHERE username='{}';'''.format(user, )
            )
            users = self.cur.fetchone()
            for user_id in users:
                self.cur.execute(
                    '''SELECT (question_id) FROM public."USERS_QUESTION_ANSWER" WHERE user_id='{}';'''.format(user_id, )
                )
            questions = []
            answers = []
            answers_d = []
            dates = []
            questions_ids = self.cur.fetchall()
            for question_id in questions_ids:
                for id in question_id:
                    self.cur.execute(
                        '''SELECT (question) FROM public."USERSQUESTION" WHERE id='{}';'''.format(id, )
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
                self.cur.execute(
                    '''SELECT (datee) FROM public."ANSWER" WHERE user_id='{}';'''.format(user_id)
                )
                dates1 = self.cur.fetchall()
                for date1 in dates1:
                    dates.append(date1)
                for question_tuple, answer_tuple, id_tuple, dates_tuple in zip(questions, answers, questions_ids,
                                                                               dates):
                    for question1, answer1, id, date in zip(question_tuple, answer_tuple, id_tuple, dates_tuple):
                        answers_d.append({"id": id, "question": question1, "answer": answer1, "date": str(date)})
            return json.dumps(answers_d)
        finally:
            self.conn.close()

    def get_user_with_most_answered_questions_dao(self):
        try:
            def most_frequent(List):
                counter = 0
                num = List[0]

                for i in List:
                    curr_frequency = List.count(i)
                    if (curr_frequency > counter):
                        counter = curr_frequency
                        num = i
                return num

            ids = []
            user_avatar = []
            user_name = []
            result = []
            self.cur.execute(
                '''SELECT (user_id) FROM public."USERS_QUESTION_ANSWER";'''
            )
            user_ids = self.cur.fetchall()
            for id_tuple in user_ids:
                for id in id_tuple:
                    ids.append(id)

            # Get top №1
            frequent_id = most_frequent(ids)
            self.cur.execute(
                '''SELECT (avatar) FROM public."USER" WHERE id='{}';'''.format(frequent_id)
            )
            avatar_querry = self.cur.fetchone()
            for avatar in avatar_querry:
                user_avatar.append(avatar)
            self.cur.execute(
                '''SELECT (name) FROM public."USER" WHERE id='{}';'''.format(frequent_id)
            )
            name_querry = self.cur.fetchone()
            for name in name_querry:
                user_name.append(name)
            user_info = {"id": frequent_id, "name": user_name[0], "avatar": user_avatar[0]}
            result.append(user_info)

            # Get top №2
            while frequent_id in ids: ids.remove(frequent_id)
            frequent_id1 = most_frequent(ids)
            user_name1 = []
            user_avatar1 = []
            self.cur.execute(
                '''SELECT (avatar) FROM public."USER" WHERE id='{}';'''.format(frequent_id1)
            )
            avatar_querry1 = self.cur.fetchone()
            for avatar in avatar_querry1:
                user_avatar1.append(avatar)
            self.cur.execute(
                '''SELECT (name) FROM public."USER" WHERE id='{}';'''.format(frequent_id1)
            )
            name_querry1 = self.cur.fetchone()
            for name in name_querry1:
                user_name1.append(name)
            user_info1 = {"id": frequent_id1, "name": user_name1[0], "avatar": user_avatar1[0]}
            result.append(user_info1)

            # Get top №3
            while frequent_id1 in ids: ids.remove(frequent_id1)
            frequent_id2 = most_frequent(ids)
            user_name2 = []
            user_avatar2 = []
            self.cur.execute(
                '''SELECT (avatar) FROM public."USER" WHERE id='{}';'''.format(frequent_id2)
            )
            avatar_querry2 = self.cur.fetchone()
            for avatar in avatar_querry2:
                user_avatar2.append(avatar)
            self.cur.execute(
                '''SELECT (name) FROM public."USER" WHERE id='{}';'''.format(frequent_id2)
            )
            name_querry2 = self.cur.fetchone()
            for name in name_querry2:
                user_name2.append(name)
            user_info2 = {"id": frequent_id2, "name": user_name2[0], "avatar": user_avatar2[0]}
            result.append(user_info2)

            # Return top 3.
            return json.dumps(result)
        finally:
            self.conn.close()

    def set_dayly_mood_dao(self, user, mood, date):
        try:
            self.cur.execute(
                '''SELECT (id) FROM public."USER" WHERE username='{}';'''.format(user, )
            )
            user_ids = self.cur.fetchone()
            for id in user_ids:
                self.cur.execute(
                    '''INSERT INTO public."MOOD"(user_id, mood, date) VALUES('{}','{}','{}');'''.format(id, mood, date)
                )
                self.conn.commit()
                return json.dumps(["Done"])
        finally:
            self.conn.close()

    def get_mood_report_dao(self, user):
        try:
            result = []
            self.cur.execute(
                '''SELECT (id) FROM public."USER" WHERE username='{}';'''.format(user, )
            )
            user_ids = self.cur.fetchone()
            for id in user_ids:
                self.cur.execute(
                    '''SELECT (mood) FROM public."MOOD" WHERE user_id='{}';'''.format(id)
                )
                mood_querry = self.cur.fetchall()
                self.cur.execute(
                    '''SELECT (date) FROM public."MOOD" WHERE user_id='{}';'''.format(id)
                )
                date_querry = self.cur.fetchall()
                for mood_tuple, date_tuple in zip(mood_querry, date_querry):
                    for mood, date in zip(mood_tuple, date_tuple):
                        result.append({"mood": mood, "date": date})
                return json.dumps(result)
        finally:
            self.conn.close()

    def get_question_by_id_admin_dao(self, id):
        try:
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

    def get_question_by_id_user_dao(self, id):
        try:
            result = []
            self.cur.execute(
                '''SELECT (question) FROM public."USERSQUESTION" WHERE id='{}';'''.format(id)
            )
            q_querry = self.cur.fetchone()
            for question in q_querry:
                result.append({"question": question})
            return json.dumps(result)
        finally:
            self.conn.close()

    def all_questions_by_user_dao(self):
        try:
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

    def get_random_users(self):
        try:
            result = []
            old_ids = []
            ids = []
            self.cur.execute(
                '''SELECT (user_id) FROM public."USERSQUESTION" '''
            )
            id_querry = self.cur.fetchall()
            for id_tuple in id_querry:
                for id in id_tuple:
                    old_ids.append(id)
            for id in old_ids:
                if id not in ids:
                    ids.append(id)
            for iter in range(3):
                random_user = random.choice(ids)
                self.cur.execute(
                    '''SELECT (id) FROM public."USER" WHERE id='{}';'''.format(random_user)
                )
                user_id_querry = self.cur.fetchone()
                self.cur.execute(
                    '''SELECT (name) FROM public."USER" WHERE id='{}';'''.format(random_user)
                )
                user_name_querry = self.cur.fetchone()
                self.cur.execute(
                    '''SELECT (avatar) FROM public."USER" WHERE id='{}';'''.format(random_user)
                )
                user_avatar_querry = self.cur.fetchone()
                ids.remove(random_user)
                for id, name, avatar in zip(user_id_querry, user_name_querry, user_avatar_querry):
                    result.append({"id":id,"name":name,"avatar":avatar})
            return json.dumps(result)
        finally:
            self.conn.close()
