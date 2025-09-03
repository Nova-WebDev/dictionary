import sqlite3
from setting import CONNECTION_DATABASE
from db.user_db import get_user_id_by_username


def get_fa_translations_by_en_word(english_word):
    with sqlite3.connect(CONNECTION_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT persian_word, author_username
            FROM dictionary_with_authors_view
            WHERE english_word = ?
        """, (english_word,))
        rows = cursor.fetchall()

        if not rows:
            raise Exception("[*][get_fa_translations_by_en_word]Database error: english_word not found in dictionary")

        return [{"persian_word": row[0], "author": row[1]} for row in rows]


def get_en_translations_by_fa_word(persian_word):
    with sqlite3.connect(CONNECTION_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT english_word, author_username
            FROM dictionary_with_authors_view
            WHERE persian_word = ?
        """, (persian_word,))
        rows = cursor.fetchall()

        if not rows:
            raise Exception("[*][get_en_translations_by_fa_word]Database error: persian_word not found in dictionary")

        return [{"english_word": row[0], "author": row[1]} for row in rows]


def get_all_words_with_authors():
    with sqlite3.connect(CONNECTION_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT d.id, d.english_word, d.persian_word, u.username
            FROM dictionary_entries d
            LEFT JOIN users u ON d.author_id = u.id
        """)
        rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "english_word": row[1],
                "persian_word": row[2],
                "author": row[3]
            }
            for row in rows
        ]


def insert_word(english_word, persian_word, author_username):
    author_id = get_user_id_by_username(author_username)

    with sqlite3.connect(CONNECTION_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute("""
            INSERT INTO dictionary_entries (english_word, persian_word, author_id)
            VALUES (?, ?, ?)
        """, (english_word, persian_word, author_id))


def update_word_by_id(word_id, fields):
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


def delete_word_by_id(word_id):
    with sqlite3.connect(CONNECTION_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM dictionary_entries
            WHERE id = ?
        """, (word_id,))
