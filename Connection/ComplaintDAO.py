import json
import os
import psycopg2


class ComplaintDAO:
    def __init__(self):
        host_for_connection_str = os.environ.get(HOST)

        db_for_connection_str = os.environ.get(DATABASE)

        user_for_connection_str = os.environ.get(USER)

        port_for_connection_str = os.environ.get(PORT)

        password_for_connection_str = os.environ.get(PASSWORD)
        self.conn = psycopg2.connect(
            f"dbname={db_for_connection_str} user={user_for_connection_str} password={password_for_connection_str} host={host_for_connection_str} port={port_for_connection_str}")
        self.cur = self.conn.cursor()

    def complaint_dao(self, username, question_id, text):
        try:
            self.__init__()
            self.cur.execute(
                '''SELECT (id) FROM public."USER" WHERE username='{}';'''.format(
                    username)
            )
            user_id_querry = self.cur.fetchone()
            for user_id in user_id_querry:
                self.cur.execute(
                    '''SELECT (id) FROM public."COMPLAINT" WHERE user_id='{}' AND question_id='{}';'''.format(user_id,
                                                                                                              question_id)
                )
                isNew = self.cur.fetchone()
                if isNew == None:
                    self.cur.execute(
                        '''INSERT INTO public."COMPLAINT"(user_id, question_id, text) VALUES('{}', '{}', '{}')'''.format(
                            user_id, question_id, text)
                    )
                    self.conn.commit()
                    return json.dumps(["Reported"])
                else:
                    return json.dumps(["Already Reported"])
        finally:
            self.conn.close()
