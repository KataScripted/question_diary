from flask import Flask
from flask_cors import CORS

from Addons.Backend.Services.AnswerService import AnswerService
from Addons.Backend.Services.ComplaintService import ComplaintService
from Addons.Backend.Services.QuestionService import QuestionService
from Addons.Backend.Services.UserService import UserService
from Addons.Backend.Services.UsersQuestionAnswerService import UsersQuestionAnswerService
from Addons.Backend.Services.UsersQuestionService import UsersQuestionService

app = Flask(__name__)
CORS(app)

UserServiceA = UserService()
QuestionServiceA = QuestionService()
AnswerServiceA = AnswerService()
UsersQuestionServiceA = UsersQuestionService()
UsersQuestionAnswerServiceA = UsersQuestionAnswerService()
ComplaintServiceA = ComplaintService()


@app.route('/insertuser', methods=["GET", "POST"])
def insert_user():
    result = UserServiceA.insert_user_service()
    return result


# @app.route('/isnew', methods=["GET", "POST"])
# def check_for_new_user():
#     result = handler.check_for_new_user()
#     return result


@app.route('/insertanswer', methods=["GET", "POST"])
def insert_answer1():
    return AnswerServiceA.insert_answer_service()


@app.route('/questions', methods=["GET", "POST"])
def get_all_questions():
    return QuestionServiceA.get_all_questions_service()


@app.route('/answered', methods=["GET", "POST"])
def answered():
    return QuestionServiceA.get_answered_question_service()


# @app.route('/notification', methods=["GET", "POST"])
# def get_users_for_notification():
#     result = handler.get_users_for_notification()
#     return result


@app.route('/questionbydate', methods=["GET", "POST"])
def get_answer_by_date():
    return AnswerServiceA.get_answer_answer_by_date_service()


@app.route('/newquestion', methods=["GET", "POST"])
def get_new_question():
    return QuestionServiceA.get_new_question_service()


@app.route('/allanswers', methods=["GET", "POST"])
def get_all_answers_on_question():
    return AnswerServiceA.get_all_answers_on_question_service()


@app.route('/createquestion', methods=["GET", "POST"])
def create_question():
    return UsersQuestionServiceA.create_users_question_service()


@app.route('/insertanswerusers', methods=["GET", "POST"])
def insert_answer_to_users_question():
    return UsersQuestionAnswerServiceA.insert_answer_to_users_question_service()


@app.route('/questionsbyuser', methods=["GET", "POST"])
def question_by_user():
    return UsersQuestionServiceA.get_question_by_user_service()


@app.route('/answeredonusers', methods=["GET", "POST"])
def answered_on_users_question():
    return UsersQuestionAnswerServiceA.get_answer_to_users_question_service()


@app.route('/allanswersusers', methods=["GET", "POST"])
def get_all_answers_on_users_question():
    return UsersQuestionAnswerServiceA.get_all_answers_to_users_question_service()


# @app.route('/top', methods=["GET", "POST"])
# def get_users_with_most_answered():
#     result = handler.get_users_with_most_answered()
#     return result
#
#
# @app.route('/mood', methods=["GET", "POST"])
# def set_dayly_mood():
#     result = handler.dayly_mood()
#     return result
#
#
# @app.route('/getmood', methods=["GET", "POST"])
# def get_dayly_mood():
#     result = handler.get_mood_report()
#     return result


@app.route('/questionbyidadmin', methods=["GET", "POST"])
def get_qustion_by_id_admin():
    return QuestionServiceA.get_question_by_id_admin_service()


@app.route('/questionbyiduser', methods=["GET", "POST"])
def get_qustion_by_id_user():
    return UsersQuestionServiceA.get_question_by_id_user_service()


@app.route('/allusersquestions', methods=["GET", "POST"])
def get_all_questions_by_users():
    return UsersQuestionServiceA.get_all_questions_by_user_service()


@app.route('/userinfo', methods=["GET", "POST"])
def get_user_info():
    return UserServiceA.get_random_users_service()


@app.route('/feed', methods=["GET", "POST"])
def feed():
    return UsersQuestionAnswerServiceA.feed_service()


@app.route('/questionbycategory', methods=["GET", "POST"])
def question_by_category():
    return QuestionServiceA.get_question_by_category_service()


@app.route('/updateanswer', methods=["GET", "POST"])
def update_answer():
    return AnswerServiceA.update_answer_service()


@app.route('/updateanswerusers', methods=["GET", "POST"])
def update_answer_user():
    return UsersQuestionAnswerServiceA.update_answer_user_service()


@app.route('/deleteanswer', methods=["GET", "POST"])
def delete_answer():
    return AnswerServiceA.delete_answer_service()


@app.route('/deleteanswerusers', methods=["GET", "POST"])
def delete_answer_user():
    return UsersQuestionAnswerServiceA.delete_answer_user_service()


@app.route('/complaint', methods=["GET", "POST"])
def comlaint():
    return ComplaintServiceA.complaint_service()


if __name__ == '__main__':
    app.run(debug=True)
