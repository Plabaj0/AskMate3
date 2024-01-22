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
    query="""
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
    query="""
            SELECT *
            FROM answer"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_answer_id(cursor, answer_id): #answers
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
        print(f"Error in get_answer_id: {e}") # mozna usunac
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
     query="""
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
def add_question(cursor, id, sub, view, vote, tittle, mes, imag):
    query = """
                INSERT INTO question (id, submission_time, view_number, vote_number, title, message, image)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
    cursor.execute(query, (id, sub, view, vote, tittle, mes, imag))


@database_common.connection_handler
def add_message(cursor, next_id, submission_time, vote_number, question_id, message, image):
    query = """
            INSERT INTO answer (id, submission_time, vote_number, question_id, message, image)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
    cursor.execute(query, (next_id, submission_time, vote_number, question_id, message, image))


@database_common.connection_handler
def add_comment(cursor: object, comment_id: object, question_id: object, answer_id: object, message: object, submission_time: object, edited_count: object = 0) -> object:
    query = """
    INSERT INTO comment (id, question_id, answer_id, message, submission_time, edited_count)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (comment_id, question_id, answer_id, message, submission_time, edited_count))
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
    query="""
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
     query="""
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
    query="""
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
def add_register_user_to_database(cursor, id, name, password, date_register):
    query="""
            INSERT INTO public.user (id, name, password, date_register)
            VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (id, name, password, date_register))

@database_common.connection_handler
def all_data_in_user(cursor):
    query="""
            SELECT id, name, password, date_register
            FROM public.user
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_password(cursor):
    query="""
            Select password
            From public.user
    """
    cursor.execute(query)
    return cursor.fetchall()