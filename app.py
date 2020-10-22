from flask import Flask
from Controllers.Controllers import Controller
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

handler = Controller()



@app.route('/insertuser', methods=["GET", "POST"])
def insert_user():
    result = handler.insert_user()
    return result


@app.route('/insertanswer', methods=["GET", "POST"])
def insert_answer1():
    result = handler.insert_answer()
    return result


@app.route('/questions', methods=["GET"])
def get_all_questions():
    result = handler.get_all_questions()
    return result


@app.route('/answered', methods=["GET", "POST"])
def answered():
    result = handler.answered()
    return result

@app.route('/notification', methods=["GET"])
def get_users_for_notification():
    result = handler.get_users_for_notification()
    return result


@app.route('/questionbydate', methods=["GET", "POST"])
def get_question_by_date():
    result = handler.get_question_by_date()
    return result


@app.route('/newquestion', methods=["GET", "POST"])
def get_new_question():
    result = handler.get_new_question()
    return result


@app.route('/allanswers', methods=["GET", "POST"])
def get_all_answers_on_question():
    result = handler.get_all_answers_on_question()
    return result


@app.route('/createquestion', methods=["GET", "POST"])
def create_question():
    result = handler.create_question()
    return result


@app.route('/insertanswerusers', methods=["GET", "POST"])
def insert_answer_to_users_question():
    result = handler.insert_answer_to_users_question()
    return result


@app.route('/questionsbyuser', methods=["GET", "POST"])
def question_by_user():
    result = handler.question_by_user()
    return result


@app.route('/answeredonusers', methods=["GET", "POST"])
def answered_on_users_question():
    result = handler.answered_on_users_question()
    return result


@app.route('/top', methods=["GET", "POST"])
def get_users_with_most_answered():
    result = handler.get_users_with_most_answered()
    return result


if __name__ == '__main__':
    app.run(debug=True)
