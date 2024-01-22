from datetime import datetime
import data_manager


def submission_time():
    now = datetime.now()
    submission = now.strftime("%Y-%m-%d %H:%M:%S")
    return submission


def question_id(question_id, query):
    question = None
    for q in query:
        if q['id'] == question_id:
            question = q
    return question


def answer_id(question_id, query):
    question = []
    for q in query:
        if q['question_id'] == question_id:
            question.append(q)
    return question


def comment_id(answer_id, query):
    answer = []
    for q in query:
        if q['answer_id'] == answer_id:
            answer.append(q)
    return answer


def next_id(ask_query):
    max_id = 0
    for q in ask_query:
        if q['id'] > max_id:
            max_id = q['id']
    return max_id + 1


def get_answers_by_question_id(question_id):
    return data_manager.get_answers_by_question_id(question_id)


def get_question_by_id(question_id):
    questions = data_manager.get_questions()
    for question in questions:
        if question['id'] == question_id:
            return question
    return None


def filter_comments_by_answer_id(answers, comments):
    filtered_comments = {answer['id']: [] for answer in answers}
    for comment in comments:
        if comment['answer_id'] in filtered_comments:
            filtered_comments[comment['answer_id']].append(comment)
    return filtered_comments


def get_tag_id(name):
    tags_name = data_manager.tag_name()
    for tag in tags_name:
        if tag['name'] == name:
            return tag['id']
    return None

def date_now():
    now = datetime.now()
    submission = now.strftime("%d-%m-%y")
    return submission
