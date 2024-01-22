import app
from flask import Flask, render_template, request, redirect, url_for, session
import data_manager as dm
import util
import bcrypt
from werkzeug.utils import secure_filename
import os

app.secret_key = 'your_secret_key'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "static/images"

@app.route('/')
def hello_world():
    date=util.date_now()
    newest_questions = dm.get_newest_questions()
    return render_template('home.html', newest_questions=newest_questions, date=date)


@app.route('/questions', methods=["GET", "POST"])
def questions():
    sentence = request.args.get('sentence')
    sentence1 = request.args.get('sentence1')
    order_by = request.args.get('order_by')
    order_direction = request.args.get('order_direction')
    tag_remove = request.args.get('tag_remove')
    date=util.date_now()

    if order_by is None:
        order_by = 'id'
    if order_direction is None:
        order_direction = 'asc'

    if tag_remove:
        dm.remove_tag(tag_remove)
        return redirect(url_for('questions', sentence1=sentence1))

    sorted_questions = dm.sort_questions(order_by, order_direction)
    return render_template('questions.html',date=date, questions=sorted_questions, order_by=order_by, order_direction=order_direction, sentence=sentence)


@app.route('/question/<question_id>')
def question(question_id):
    date = util.date_now()
    tag_name= dm.tag_id(question_id)
    question_id = int(question_id)
    question = util.question_id(question_id, dm.get_questions())
    answers = util.get_answers_by_question_id(question_id)
    comments = dm.get_comment()
    filtered_comments = util.filter_comments_by_answer_id(answers, comments)
    dm.update_views(question_id)
    tag_name1 = request.args.get('tag_name')
    if request.method == 'GET' and tag_name1:
        tag_id = util.get_tag_id(tag_name1)
        dm.add_question_tag(question_id, tag_id)
    return render_template('question.html',date=date, question=question, question_id=question_id, answer_id=answers, comments=comments, tag_name=tag_name,answers=answers, filtered_comments= filtered_comments)


@app.route('/question/<question_id>/new-comment', methods=["GET", "POST"])
def new_answer(question_id):
    date = util.date_now()
    question_id = int(question_id)
    question = util.question_id(question_id, dm.get_questions())
    answer_id= util.answer_id(question_id, dm.get_answer())
    if request.method == 'POST':
        next_id = util.next_id(dm.get_answer())
        submission_time = util.submission_time()
        vote_number = 0
        question_id1 = question_id
        message = request.form.get('answer', '')
        image = None
        dm.add_message(next_id, submission_time, vote_number, question_id1, message, image)
        return redirect(url_for('question', question_id=question_id))
    return render_template('new-answer.html',date=date, question=question, question_id=question_id, answer_id=answer_id)


@app.route('/questions/add-question', methods=["GET", "POST"])
def add_question():
    if request.method == 'GET':
        return render_template('add-question.html')

    que_id = util.next_id(dm.get_questions())
    submission_time = util.submission_time()
    view_number = 0
    vote_number = 0
    title = request.form.get('title')
    message = request.form.get('question')
    image = None
    file = request.files.get('image')
    if file and file.filename != '':
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        image = filename
    dm.add_question(que_id, submission_time, view_number, vote_number, title, message, image)
    return redirect(url_for('questions'))

                        
@app.route('/answers/<int:answer_id>/add-comment', methods=['GET', 'POST'])
def add_comment(answer_id):
    date = util.date_now()
    answer = dm.get_answer_id(answer_id)
    question_id = answer['question_id']
    question = util.get_question_by_id(question_id)
    if request.method == 'POST':
        comment_id = util.next_id(dm.get_comment())
        message = request.form.get('comment_message')
        sub = util.submission_time()
        dm.add_comment(comment_id, question_id, answer_id, message, sub, edited_count=0)
        return redirect(url_for('question', question=question, answer=answer, question_id=answer['question_id']))
    return render_template('new-comment.html',date=date, answer_id=answer_id, question=question, answer=answer)


@app.route('/question/<int:question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    question = util.get_question_by_id(question_id)
    if request.method == 'POST':
        title=request.form.get('title')
        edited_content = request.form.get('question')
        sub = util.submission_time()
        dm.update_question(question_id, edited_content, sub, title)
        return redirect(url_for('question', question=question, question_id=question_id))
    return render_template('edit-question.html', question=question, question_id=question_id)


@app.route('/answers/<int:answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id):
    answer = dm.get_answer_id(answer_id)
    question_id = answer['question_id']
    question=util.get_question_by_id(question_id)
    if request.method == 'POST':
        edited_content = request.form.get('answer')
        sub = util.submission_time()
        dm.update_answer(answer_id, edited_content, sub)
        return redirect(url_for('question', question=question, question_id=question_id, answer=answer))
    return render_template('edit-answer.html', question=question, answer=answer)


@app.route('/edit_comment/<int:comment_id>', methods=['GET', 'POST'])
def edit_comment(comment_id):
    date = util.date_now()
    comment = dm.get_comment_by_id(comment_id)
    answer_id = comment['answer_id']
    answer = dm.get_answer_id(answer_id)
    question_id = comment['question_id']
    question = util.get_question_by_id(question_id)
    if request.method == 'GET':
        return render_template('edit-comment.html',date=date, comment=comment, question=question, answer=answer)
    if request.method == 'POST':
        new_message = request.form.get('message')
        edited_count = comment['edited_count'] + 1
        sub = util.submission_time()
        dm.update_comment(comment_id, new_message, sub, edited_count)
        return redirect(url_for('question',comment=comment,date=date, question=question, question_id=question_id, answer=answer))

@app.route('/search', methods=["GET", "POST"])
def search():
    results_ans= None
    results_que= None
    checkbox=request.args.get('checkbox')
    date = util.date_now()

    if checkbox == 'on':
        sentence = request.args.get('q')
        return redirect(url_for('questions', sentence=sentence, checkbox=checkbox))

    if checkbox != 'on':
        sentence = request.args.get('q')
        results_ans = dm.search_answer(sentence)
        results_que = dm.search_question(sentence)

    return render_template('search.html',date=date, results_ans=results_ans, results_que=results_que)

@app.route('/delete_question/<int:question_id>', methods=['GET', 'POST'])
def delete_question_answers_and_comments(question_id):
    if request.method == 'POST':
        dm.delete_question_tag(question_id)
        dm.delete_comments_by_answer_id(question_id)
        dm.delete_answers_by_question_id(question_id)
        dm.delete_question(question_id)
        return render_template('questions.html', questions=dm.get_questions())
    return render_template('confirmation.html', question_id=question_id, function='delete_question_answers_and_comments')


@app.route('/questions/<int:question_id>/upvote')
def upvote(question_id):
    dm.upvote(question_id)
    return redirect(url_for('question', question_id=question_id))


@app.route('/questions/<int:question_id>/downvote')
def downvote(question_id):
    dm.downvote(question_id)
    return redirect(url_for('question', question_id=question_id))


@app.route('/delete_answer/<int:answer_id>', methods=['GET', 'POST'])
def delete_answer_and_comments(answer_id):
    answer = dm.get_answer_id(answer_id)
    question_id = answer['question_id']
    if request.method == 'POST':
        dm.delete_comments_by_answer_id(answer_id)
        dm.delete_answer(answer_id)
        return redirect(url_for('question', question_id=question_id))
    return render_template('confirmation.html', answer_id=answer_id, question_id=question_id,
                           function='delete_answer_and_comments')


@app.route('/delete_comment/<int:comment_id>', methods=['GET', 'POST'])
def delete_comment(comment_id):
    comment = dm.get_comment_by_id(comment_id)
    question_id = comment['question_id']

    if request.method == 'POST':
        dm.delete_comment(comment_id)
        return redirect(url_for('question', question_id=question_id))

    return render_template('confirmation.html', comment_id=comment_id, question_id=question_id,
                           function='delete_comment')


@app.route('/question/<question_id>/new-tag', methods=['GET', 'POST'])
def add_tag(question_id):
    tags_name = dm.tag_name()
    date = util.date_now()
    question = util.question_id(question_id, dm.get_questions())
    que_id = util.next_id(tags_name)

    if request.method == 'POST':
        tag_name = request.form.get('tag')
        dm.add_tag(que_id, tag_name)

    return render_template('new-tag.html',date=date, tags_name=tags_name, question=question, question_id=question_id)

@app.route('/register', methods=['GET', 'POST'])
def register():
    all_users=dm.all_data_in_user()
    date = util.date_now()
    id_to_db = util.next_id(all_users)

    if request.method =="POST":
        login = request.form.get('login')
        password = request.form.get('password')
        hash_code = bcrypt.hashpw(password.encode("UTF-8"), bcrypt.gensalt())
        dm.add_register_user_to_database(id_to_db, login, hash_code, date)
        return redirect(url_for('hello_world'))

    return render_template('registration.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == "POST":
        password = request.form.get('password')
        db_password = dm.get_password()

    if bcrypt.checkpw(password.encode("UTF-8"), db_password):
        session['username'] = 'example_user'
        
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
