from flask import Flask, render_template, request, redirect, url_for, session, flash
import data_manager as dm
import util
import bcrypt
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "static/images"
app.secret_key = b'safdghjkfdshjdfhsd123'


@app.route('/')
def hello_world():
    date = util.date_now()
    newest_questions = dm.get_newest_questions()
    name = session.get('username')
    return render_template('home.html', newest_questions=newest_questions, name=name, date=date)


@app.route('/questions', methods=["GET", "POST"])
def questions():
    name = session.get('username')
    sentence = request.args.get('sentence')
    sentence1 = request.args.get('sentence1')
    order_by = request.args.get('order_by')
    order_direction = request.args.get('order_direction')
    tag_remove = request.args.get('tag_remove')
    date = util.date_now()

    if order_by is None:
        order_by = 'id'
    if order_direction is None:
        order_direction = 'asc'

    if tag_remove:
        dm.remove_tag(tag_remove)
        return redirect(url_for('questions', sentence1=sentence1))

    sorted_questions = dm.sort_questions(order_by, order_direction)
    return render_template('questions.html', date=date, name=name, questions=sorted_questions, order_by=order_by,
                           order_direction=order_direction, sentence=sentence)


@app.route('/question/<question_id>')
def question(question_id):
    name = session.get('username')
    date = util.date_now()
    tag_name = dm.tag_id(question_id)
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
    return render_template('question.html', date=date, name=name, question=question, question_id=question_id,
                           answer_id=answers, comments=comments, tag_name=tag_name, answers=answers,
                           filtered_comments=filtered_comments)


@app.route('/question/<question_id>/new-comment', methods=["GET", "POST"])
def new_answer(question_id):
    if session:
        username = session.get('username')
    else:
        username = None
    user_id = util.get_id_user_for_name(username)

    name = session.get('username')
    date = util.date_now()
    question_id = int(question_id)
    question = util.question_id(question_id, dm.get_questions())
    answer_id = util.answer_id(question_id, dm.get_answer())
    if request.method == 'POST':
        next_id = util.next_id(dm.get_answer())
        submission_time = util.submission_time()
        vote_number = 0
        question_id1 = question_id
        message = request.form.get('answer', '')
        image = None
        dm.add_message(next_id, submission_time, vote_number, question_id1, message, image, user_id)
        return redirect(url_for('question', question_id=question_id))
    return render_template('new-answer.html', date=date, name=name, question=question, question_id=question_id,
                           answer_id=answer_id)


@app.route('/questions/add-question', methods=["GET", "POST"])
def add_question():
    if request.method == 'GET':
        return render_template('add-question.html')

    if session:
        username = session.get('username')
    else:
        username = None

    que_id = util.next_id(dm.get_questions())
    submission_time = util.submission_time()
    view_number = 0
    vote_number = 0
    title = request.form.get('title')
    message = request.form.get('question')
    image = None
    user_id = util.get_id_user_for_name(username)
    file = request.files.get('image')
    if file and file.filename != '':
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        image = filename
    dm.add_question(que_id, submission_time, view_number, vote_number, title, message, image, user_id)
    return redirect(url_for('questions'))


@app.route('/answers/<int:answer_id>/add-comment', methods=['GET', 'POST'])
def add_comment(answer_id):
    if session:
        username = session.get('username')
    else:
        username = None

    user_id = util.get_id_user_for_name(username)
    name = session.get('username')
    date = util.date_now()
    answer = dm.get_answer_id(answer_id)
    question_id = answer['question_id']
    question = util.get_question_by_id(question_id)
    if request.method == 'POST':
        comment_id = util.next_id(dm.get_comment())
        message = request.form.get('comment_message')
        sub = util.submission_time()
        dm.add_comment(comment_id, question_id, answer_id, message, sub, user_id, edited_count=0)
        return redirect(url_for('question', question=question, answer=answer, question_id=answer['question_id']))
    return render_template('new-comment.html', date=date, name=name, answer_id=answer_id, question=question,
                           answer=answer)


@app.route('/question/<int:question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    question = util.get_question_by_id(question_id)
    if request.method == 'POST':
        title = request.form.get('title')
        edited_content = request.form.get('question')
        sub = util.submission_time()
        dm.update_question(question_id, edited_content, sub, title)
        return redirect(url_for('question', question=question, question_id=question_id))
    return render_template('edit-question.html', question=question, question_id=question_id)


@app.route('/answers/<int:answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id):
    name = session.get('username')
    answer = dm.get_answer_id(answer_id)
    question_id = answer['question_id']
    question = util.get_question_by_id(question_id)
    if request.method == 'POST':
        edited_content = request.form.get('answer')
        sub = util.submission_time()
        dm.update_answer(answer_id, edited_content, sub)
        return redirect(url_for('question', question=question, question_id=question_id, answer=answer))
    return render_template('edit-answer.html', name=name, question=question, answer=answer)


@app.route('/edit_comment/<int:comment_id>', methods=['GET', 'POST'])
def edit_comment(comment_id):
    name = session.get('username')
    date = util.date_now()
    comment = dm.get_comment_by_id(comment_id)
    answer_id = comment['answer_id']
    answer = dm.get_answer_id(answer_id)
    question_id = comment['question_id']
    question = util.get_question_by_id(question_id)
    if request.method == 'GET':
        return render_template('edit-comment.html', date=date, name=name, comment=comment, question=question,
                               answer=answer)
    if request.method == 'POST':
        new_message = request.form.get('message')
        edited_count = comment['edited_count'] + 1
        sub = util.submission_time()
        dm.update_comment(comment_id, new_message, sub, edited_count)
        return redirect(
            url_for('question', comment=comment, date=date, question=question, question_id=question_id, answer=answer))


@app.route('/search', methods=["GET", "POST"])
def search():
    name = session.get('username')
    results_ans = None
    results_que = None
    checkbox = request.args.get('checkbox')
    date = util.date_now()

    if checkbox == 'on':
        sentence = request.args.get('q')
        return redirect(url_for('questions', sentence=sentence, checkbox=checkbox))

    if checkbox != 'on':
        sentence = request.args.get('q')
        results_ans = dm.search_answer(sentence)
        results_que = dm.search_question(sentence)

    return render_template('search.html', date=date, results_ans=results_ans, results_que=results_que)


@app.route('/question/<id>/delete', methods=["POST"])
def delete_question(id):
    if request.method == "POST":
        image_path = dm.check_if_image_exists(id)
        if image_path:
            util.delete_image(image_path)
        dm.delete_question(id)
        return redirect(url_for("questions"))


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

    return render_template('new-tag.html', date=date, tags_name=tags_name, question=question, question_id=question_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('registration_form.html')

    users = dm.all_data_in_user()
    id = util.next_id(users)
    current_date = util.submission_time()
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    if password != confirm_password:
        flash('Passwords do not match, try again!')
        return render_template('registration_form.html')

    hashed_password = bcrypt.hashpw(password.encode("UTF-8"), bcrypt.gensalt())
    dm.add_user_to_database(id, username, hashed_password, current_date)
    return redirect(url_for('hello_world'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    name = session.get('username')
    username_provided = request.form.get('username')
    password_provided = request.form.get('password')
    user_data = dm.fetch_user_from_database(username_provided)
    if user_data and bcrypt.checkpw(password_provided.encode('utf-8'), bytes(user_data["password"])):
        session['username'] = username_provided
        return redirect(url_for('hello_world'))
    else:
        flash('Invalid username or password')  # przekazanie do forumularza
        return render_template('login.html', name=name)


@app.route('/user/<int:user_id>')
def user(user_id):
    name = session.get('username')
    search_user_id = int(user_id)
    search_user_data = dm.get_user_data(user_id)
    search_username = search_user_data['login']
    registration_date = search_user_data['registration_date']
    reputation = search_user_data['reputation']
    questions = dm.get_user_questions(user_id)
    answers = dm.get_user_answers(user_id)
    comments = dm.get_user_comments(user_id)
    for answer in answers:
        question_id = answer['question_id']
        question = dm.get_question_by_id(question_id)
        answer['question_title'] = question['title']
    for comment in comments:
        question_id = comment['question_id']
        question = dm.get_question_by_id(question_id)
        comment['question_title'] = question['title']
    for comment in comments:
        answer_id = comment['answer_id']
        answer = dm.get_answer_id(answer_id)
        comment['answer_message'] = answer['message']
    user_id = dm.get_user_id(session['username'])
    user_data = dm.get_user_data(user_id)
    username = user_data['login']
    return render_template('user.html',name=name, search_user_id=search_user_id, search_username=search_username,
                           registration_date=registration_date, questions=questions, answers=answers, comments=comments,
                           reputation=reputation, user_id=user_id, username=username)

@app.route('/users')
def users():
    if 'username' not in session:
        return redirect(url_for('username'))
    name = session.get('username')
    users_data = dm.get_all_users_data()
    user_id = dm.get_user_id(session['username'])
    user_data = dm.get_user_data(user_id)
    username = user_data['login']
    return render_template('users.html',name=name, users_data=users_data, username=username, user_id=user_id)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('hello_world'))


if __name__ == '__main__':
    app.run(debug=True)
