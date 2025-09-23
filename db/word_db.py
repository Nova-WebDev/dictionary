import sqlite3
from setting import CONNECTION_DATABASE
from db.user_db import get_user_id_by_username


def db_english_word_exists(english_word):
    with sqlite3.connect(CONNECTION_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM dictionary_entries WHERE english_word = ?", (english_word,))
        return cursor.fetchone() is not None


def db_persian_word_exists(persian_word):
    with sqlite3.connect(CONNECTION_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM dictionary_entries WHERE persian_word = ?", (persian_word,))
        return cursor.fetchone() is not None


def db_translation_pair_exists(english_word, persian_word):
    with sqlite3.connect(CONNECTION_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 1 FROM dictionary_entries
            WHERE english_word = ? AND persian_word = ?
        """, (english_word, persian_word))
        return cursor.fetchone() is not None


def db_word_id_exists(word_id):
    with sqlite3.connect(CONNECTION_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM dictionary_entries WHERE id = ?", (word_id,))
        return cursor.fetchone() is not None


def db_word_id_belongs_to_author(word_id, author_username):
    with sqlite3.connect(CONNECTION_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 1
            FROM dictionary_with_authors_view
            WHERE id = ? AND author_username = ?
        """, (word_id, author_username))
        return cursor.fetchone() is not None


def db_author_has_words(author_username):
    with sqlite3.connect(CONNECTION_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 1
            FROM dictionary_with_authors_view
            WHERE author_username = ?
            LIMIT 1
        """, (author_username,))
        return cursor.fetchone() is not None


def db_get_fa_translations_by_en_word(english_word):
    with sqlite3.connect(CONNECTION_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT persian_word, author_username
            FROM dictionary_with_authors_view
            WHERE english_word = ?
        """, (english_word,))
        rows = cursor.fetchall()

        if not rows:
            raise Exception("[*][db_get_fa_translations_by_en_word]Database error: english_word not found in dictionary")

        result = {}
        for persian_word, author in rows:
            if persian_word not in result:
                result[persian_word] = author

        return result


def db_get_en_translations_by_fa_word(persian_word):
    with sqlite3.connect(CONNECTION_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT english_word, author_username
            FROM dictionary_with_authors_view
            WHERE persian_word = ?
        """, (persian_word,))
        rows = cursor.fetchall()

        if not rows:
            raise Exception("[*][db_get_en_translations_by_fa_word]Database error: persian_word not found in dictionary")

        result = {}
        for english_word, author in rows:
            if english_word not in result:
                result[english_word] = author

        return result


def db_get_words_by_author(author_username):
    with sqlite3.connect(CONNECTION_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, english_word, persian_word
            FROM dictionary_with_authors_view
            WHERE author_username = ?
        """, (author_username,))
        rows = cursor.fetchall()

        if not rows:
            raise Exception("[*][db_get_words_by_author]Database error: author has not submitted any words")

        result = {}
        for word_id, en, fa in rows:
            result[word_id] = {
                "english_word": en,
                "persian_word": fa
            }

        return result


def db_get_all_words_with_authors():
    with sqlite3.connect(CONNECTION_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT d.id, d.english_word, d.persian_word, u.username
            FROM dictionary_entries d
            LEFT JOIN users u ON d.author_id = u.id
        """)
        rows = cursor.fetchall()

        return [{"id": row[0], "english_word": row[1], "persian_word": row[2], "author": row[3]} for row in rows]


def db_insert_word(english_word, persian_word, author_username):
    author_id = get_user_id_by_username(author_username)

    with sqlite3.connect(CONNECTION_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute("""
            INSERT INTO dictionary_entries (english_word, persian_word, author_id)
            VALUES (?, ?, ?)
        """, (english_word, persian_word, author_id))


def db_update_word_by_id(word_id, fields):
    if not fields:
        return

    updates = []
    values = []

    if "english_word" in fields:
        updates.append("english_word = ?")
        values.append(fields["english_word"])

    if "persian_word" in fields:
        updates.append("persian_word = ?")
        values.append(fields["persian_word"])

    if "author_username" in fields:
        author_id = get_user_id_by_username(fields["author_username"])
        updates.append("author_id = ?")
        values.append(author_id)

    values.append(word_id)

    with sqlite3.connect(CONNECTION_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            UPDATE dictionary_entries
            SET {', '.join(updates)}
            WHERE id = ?
        """, values)


def db_delete_word_by_id(word_id):
    with sqlite3.connect(CONNECTION_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM dictionary_entries
            WHERE id = ?
        """, (word_id,))
