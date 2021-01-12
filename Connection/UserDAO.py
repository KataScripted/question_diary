import json
import psycopg2
import random
import os


class UserDAO:
    def __init__(self):
        host_for_connection_str = os.environ.get(HOST)

        db_for_connection_str = os.environ.get(DATABASE)

        user_for_connection_str = os.environ.get(USER)

        port_for_connection_str = os.environ.get(PORT)

        password_for_connection_str = os.environ.get(PASSWORD)
        self.conn = psycopg2.connect(
            f"dbname={db_for_connection_str} user={user_for_connection_str} password={password_for_connection_str} host={host_for_connection_str} port={port_for_connection_str}")
        self.cur = self.conn.cursor()

    def insert_user_dao(self, user, avatar, name):
        try:
            self.__init__()
            self.cur.execute(

                '''SELECT username FROM public."USER" WHERE username='{}';'''.format(
                    user, )
            )
            rows = self.cur.fetchall()
            if len(rows) > 0:
                self.conn.commit()
                result = ["Inserted"]
                return json.dumps(result)
            else:
                self.cur.execute(
                    '''INSERT INTO public."USER"(username, avatar, name) VALUES('{}','{}','{}');'''.format(
                        user,
                        avatar, name)
                )
                self.conn.commit()
                result = ["Inserted"]
                return json.dumps(result)
        finally:
            self.conn.close()

    # def check_for_new_user_dao(self, username):
    #     try:
    #         self.cur.execute(
    #
    #             '''SELECT username FROM public."USER" WHERE username='{}';'''.format(username, )
    #         )
    #         rows = self.cur.fetchall()
    #         if len(rows) > 0:
    #             self.conn.commit()
    #             return json.dumps([False])
    #         else:
    #             return json.dumps([True])
    #     finally:
    #         self.conn.close()

    def get_random_users_dao(self, username):
        try:
            self.__init__()
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
            self.cur.execute(
                '''SELECT (id) FROM public."USER" WHERE username='{}';'''.format(
                    username)
            )
            your_user_quarry = self.cur.fetchone()
            for your_user in your_user_quarry:
                if your_user in ids:
                    ids.remove(your_user)
            for itera in range(len(ids)):
                random_user = random.choice(ids)
                self.cur.execute(
                    '''SELECT (username) FROM public."USER" WHERE id='{}';'''.format(
                        random_user)
                )
                user_username_querry = self.cur.fetchone()
                self.cur.execute(
                    '''SELECT (name) FROM public."USER" WHERE id='{}';'''.format(
                        random_user)
                )
                user_name_querry = self.cur.fetchone()
                self.cur.execute(
                    '''SELECT (avatar) FROM public."USER" WHERE id='{}';'''.format(
                        random_user)
                )
                user_avatar_querry = self.cur.fetchone()
                ids.remove(random_user)
                for username, name, avatar in zip(user_username_querry, user_name_querry, user_avatar_querry):
                    result.append(
                        {"username": username, "name": name, "avatar": avatar})
            return json.dumps(result)
        finally:
            self.conn.close()
