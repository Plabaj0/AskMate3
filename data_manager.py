import database_common


@database_common.connection_handler
def search_question(cursor, sentence):
    query = """
        SELECT DISTINCT id, message, title
        FROM question
        WHERE title ILIKE %s OR message ILIKE %s
    """
    cursor.execute(query, ('%' + sentence + '%', '%' + sentence + '%'))
    return cursor.fetchall()


@database_common.connection_handler
def get_newest_questions(cursor):
    query = """
            SELECT id, submission_time, view_number, vote_number, title, message, image
            FROM question
            ORDER BY submission_time DESC
            LIMIT 3
            """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def search_answer(cursor, sentence):
    query = """
            SELECT DISTINCT id, message
            FROM answer
            WHERE message ILIKE %s
            """
    cursor.execute(query, ('%' + sentence + '%',))
    return cursor.fetchall()


@database_common.connection_handler
def get_questions(cursor):
    query = """
            SELECT id, submission_time, view_number, vote_number, title, message, image
            FROM question"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_question_by_id(cursor, question_id):
    query = """
        SELECT id, submission_time, view_number, vote_number, title, message, image
        FROM question
        WHERE id = %s
    """
    cursor.execute(query, (question_id,))
    return cursor.fetchone()


@database_common.connection_handler
def get_answer(cursor):
    query = """
            SELECT *
            FROM answer"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_answer_id(cursor, answer_id):  # answers
    try:
        query = """
                SELECT *
                FROM answer
                WHERE id = %s
                """
        cursor.execute(query, (answer_id,))
        answer = cursor.fetchone()
        return answer
    except Exception as e:
        print(f"Error in get_answer_id: {e}")  # mozna usunac
        return None


@database_common.connection_handler
def get_answers_by_question_id(cursor, question_id):
    query = """
        SELECT id, submission_time, vote_number, message
        FROM answer
        WHERE question_id = %s
    """
    cursor.execute(query, (question_id,))
    return cursor.fetchall()


@database_common.connection_handler
def get_comment(cursor):
    query = """
             SELECT *
             FROM comment"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_comment_by_id(cursor, comment_id):
    query = """
        SELECT id, question_id, answer_id, message, submission_time, edited_count
        FROM comment
        WHERE id = %s
    """
    cursor.execute(query, (comment_id,))
    return cursor.fetchone()


@database_common.connection_handler
def get_comment_by_answer_id(cursor, answer_id):
    query = """
        SELECT id, question_id, answer_id, message, submission_time, edited_count
        FROM comment
        WHERE answer_id = %s
    """
    cursor.execute(query, (answer_id,))
    return cursor.fetchall()


@database_common.connection_handler
def add_question(cursor, id, sub, view, vote, tittle, mes, imag, username):
    query = """
                INSERT INTO question (id, submission_time, view_number, vote_number, title, message, image, user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
    cursor.execute(query, (id, sub, view, vote, tittle, mes, imag, username))


@database_common.connection_handler
def add_message(cursor, next_id, submission_time, vote_number, question_id, message, image, user):
    query = """
            INSERT INTO answer (id, submission_time, vote_number, question_id, message, image, user_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
    cursor.execute(query, (next_id, submission_time, vote_number, question_id, message, image, user))


@database_common.connection_handler
def add_comment(cursor: object, comment_id: object, question_id: object, answer_id: object, message: object,
                submission_time: object, username, edited_count: object = 0) -> object:
    query = """
    INSERT INTO comment (id, question_id, answer_id, message, submission_time, edited_count, user_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (comment_id, question_id, answer_id, message, submission_time, edited_count, username))
    #  return cursor.fetchone() od 0


@database_common.connection_handler
def update_question(cursor, question_id, new_message, submission_time, title):
    query = """
            UPDATE question
            SET title = %s,
            submission_time = %s,
            message = %s
            WHERE id = %s
            """
    cursor.execute(query, (title, submission_time, new_message, question_id))


@database_common.connection_handler
def update_answer(cursor, answer_id, new_message, submission_time):
    query = """
            UPDATE answer
            SET message = %s,
            submission_time = %s
            WHERE id = %s
            """
    cursor.execute(query, (new_message, submission_time, answer_id))


@database_common.connection_handler
def update_comment(cursor, comment_id, new_message, submission_time, edited_count):
    query = """
        UPDATE comment
        SET message = %s, 
            submission_time = %s,
            edited_count = %s
        WHERE id = %s
    """
    cursor.execute(query, (new_message, submission_time, edited_count, comment_id))


@database_common.connection_handler
def delete_question(cursor, question_id):
    query = """
        DELETE FROM question
        WHERE id = %s
    """
    cursor.execute(query, (question_id,))


@database_common.connection_handler
def delete_answer(cursor, answer_id):
    delete_comments_query = """
        DELETE FROM comment
        WHERE answer_id = %s
    """
    cursor.execute(delete_comments_query, (answer_id,))

    delete_answer_query = """
        DELETE FROM answer
        WHERE id = %s
    """
    cursor.execute(delete_answer_query, (answer_id,))


@database_common.connection_handler
def sort_questions(cursor, order_by, order_direction):
    query = """
            SELECT *
            FROM question
            ORDER BY {} {}
        """.format(order_by, order_direction)

    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def tag_name(cursor):
    query = """
        SELECT DISTINCT id, name
        FROM tag
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def tag_id(cursor, question_id):
    query = """
        SELECT tag.name
        FROM question_tag
        INNER JOIN tag ON question_tag.tag_id = tag.id
        WHERE question_tag.question_id = %s
    """
    cursor.execute(query, (question_id,))
    return cursor.fetchone()


@database_common.connection_handler
def add_tag(cursor, id, name):
    query = """
        INSERT INTO tag (id, name)
        VALUES (%s, %s)
        """
    cursor.execute(query, (id, name))


@database_common.connection_handler
def add_question_tag(cursor, question_id, tag_id):
    query = """
    INSERT INTO question_tag (question_id, tag_id)
    VALUES (%s, %s)
    """
    cursor.execute(query, (question_id, tag_id))


@database_common.connection_handler
def remove_tag(cursor, tag_id):
    query_remove_references = """
    DELETE FROM question_tag
    WHERE tag_id = %s
    """
    cursor.execute(query_remove_references, (tag_id,))

    query_remove_tag = """
    DELETE FROM tag
    WHERE ID = %s
    """
    cursor.execute(query_remove_tag, (tag_id,))


@database_common.connection_handler
def get_comment(cursor):
    query = """
             SELECT *
             FROM comment"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def delete_comment(cursor, comment_id):
    query = """
        DELETE FROM comment
        WHERE id = %s
    """
    cursor.execute(query, (comment_id,))


@database_common.connection_handler
def delete_answers_by_question_id(cursor, question_id):
    query = """
        DELETE FROM answer
        WHERE question_id = %s
    """
    cursor.execute(query, (question_id,))


@database_common.connection_handler
def delete_comments_by_question_id(cursor, question_id):
    query = """
        DELETE FROM comment
        WHERE question_id = %s
    """
    cursor.execute(query, (question_id,))


@database_common.connection_handler
def delete_comments_by_answer_id(cursor, answer_id):
    query = """
        DELETE FROM comment
        WHERE answer_id = %s
    """
    cursor.execute(query, (answer_id,))


@database_common.connection_handler
def upvote(cursor, question_id):
    query = """
    UPDATE question
    SET vote_number = vote_number + 1
    WHERE id = %s"""
    cursor.execute(query, (question_id,))


@database_common.connection_handler
def downvote(cursor, question_id):
    query = """
    UPDATE question
    SET vote_number = vote_number - 1
    WHERE id = %s"""
    cursor.execute(query, (question_id,))


@database_common.connection_handler
def update_views(cursor, question_id):
    query = """
    UPDATE question
    SET view_number = view_number + 1
    WHERE id = %s"""
    cursor.execute(query, (question_id,))


@database_common.connection_handler
def delete_question_tag(cursor, question_id):
    query = """
            DELETE FROM question_tag
            WHERE question_id= %s
        """
    cursor.execute(query, (question_id,))


@database_common.connection_handler
def all_data_in_user(cursor):
    query = """
            SELECT id, login, password, registration_date
            FROM public.users
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_password(cursor, id_name):
    query = """
            SELECT password
            FROM public.users
            WHERE id = %s
    """
    cursor.execute(query, (id_name,))
    return cursor.fetchall()


@database_common.connection_handler
def get_name(cursor):
    query = """
                Select id, login
                From public.users
        """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_com_by_user(cursor, user_id):
    query = """
    SELECT id, message
    FROM comment
    WHERE user_id = %s
    """
    cursor.execute(query, (user_id,))
    return cursor.fetchall()


@database_common.connection_handler
def get_que_by_user(cursor, user_id):
    query = """
    SELECT id, title
    FROM question
    WHERE user_id = %s
    """
    cursor.execute(query, (user_id,))
    return cursor.fetchall()


@database_common.connection_handler
def get_ans_by_user(cursor, user_id):
    query = """
    SELECT id, message
    FROM answer
    WHERE user_id = %s
    """
    cursor.execute(query, (user_id,))
    return cursor.fetchall()


@database_common.connection_handler
def add_user_to_database(cursor, id, user_id, password, registration_date):
    query = """INSERT INTO public.users (id, login, password, registration_date)
    VALUES (%s ,%s, %s, %s)"""
    cursor.execute(query, (id, user_id, password, registration_date))


@database_common.connection_handler
def fetch_user_from_database(cursor, username):
    query = """SELECT id, login, password, registration_date 
    FROM public.users
    WHERE login = %(username)s"""
    cursor.execute(query, {'username': username})
    return cursor.fetchone()


@database_common.connection_handler
def check_if_image_exists(cursor, question_id):
    query = """SELECT image FROM question WHERE id=%s"""
    cursor.execute(query, (question_id,))
    result = cursor.fetchone()

    if result and result["image"]:
        return result["image"]
    else:
        return None


@database_common.connection_handler
def edit_question(cursor, question_id, title, message, image):
    query = """UPDATE question
    SET title=%s, 
        message=%s,
        image=%s
    WHERE id=%s;"""
    cursor.execute(query, (title, message, image, question_id))


@database_common.connection_handler
def get_user_id(cursor, login):
    query = """
        SELECT id
        FROM public.users
        WHERE login=%s
        """
    cursor.execute(query, (login,))
    result = cursor.fetchone()
    return result['id']


@database_common.connection_handler
def get_user_data(cursor, user_id):
    query = """
            SELECT id, login, registration_date, reputation
            FROM public.users
            WHERE id = %s
            """
    cursor.execute(query, (user_id,))
    user_details = cursor.fetchone()
    return user_details


@database_common.connection_handler
def delete_question(cursor, question_id):
    try:
        cursor.execute("BEGIN;")

        query3 = """DELETE FROM comment WHERE question_id=%(question_id)s"""
        cursor.execute(query3, {"question_id": question_id})

        query4 = """DELETE FROM question_tag WHERE question_id=%(question_id)s"""
        cursor.execute(query4, {"question_id": question_id})

        query1 = """DELETE FROM answer WHERE question_id=%(question_id)s"""
        cursor.execute(query1, {"question_id": question_id})

        query2 = """DELETE FROM question WHERE id=%(question_id)s"""
        cursor.execute(query2, {"question_id": question_id})

        cursor.execute("COMMIT;")
    except Exception as e:
        cursor.execute("ROLLBACK;")
        raise e


@database_common.connection_handler
def get_user_questions(cursor, user_id):
    query = """
            SELECT id, title, message
            FROM question
            WHERE user_id=%s
            """
    cursor.execute(query, (user_id,))
    user_questions = cursor.fetchall()
    return user_questions


@database_common.connection_handler
def get_user_answers(cursor, user_id):
    query = """
            SELECT id, message, question_id
            FROM answer
            WHERE user_id=%s
            """
    cursor.execute(query, (user_id,))
    user_answers = cursor.fetchall()
    return user_answers


@database_common.connection_handler
def get_user_comments(cursor, user_id):
    query = """
            SELECT id, message, question_id, answer_id
            FROM comment
            WHERE user_id=%s
            """
    cursor.execute(query, (user_id,))
    user_comments = cursor.fetchall()
    return user_comments


@database_common.connection_handler
def get_all_users_data(cursor):
    query = """
        SELECT
            u.id,
            u.login,
            u.registration_date,
            u.reputation,
            COUNT(DISTINCT q.id) AS num_questions,
            COUNT(DISTINCT a.id) AS num_answers,
            COUNT(DISTINCT c.id) AS num_comments
        FROM public.users u
        LEFT JOIN question q ON u.id = q.user_id
        LEFT JOIN answer a ON u.id = a.user_id
        LEFT JOIN comment c ON u.id = c.user_id
        GROUP BY u.id
        ORDER BY u.id;
    """
    cursor.execute(query)
    users_data = cursor.fetchall()
    return users_data