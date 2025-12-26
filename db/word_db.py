class WordRepository:
    def __init__(self, cursor):
        self._cursor = cursor

    def get_all_words_with_authors(self):
        self._cursor.execute("""
            SELECT d.id, d.english_word, d.persian_word, u.username
            FROM dictionary_entries d
            LEFT JOIN users u ON d.author_id = u.id
        """)
        rows = self._cursor.fetchall()
        return [
            {
                "id": row[0],
                "english_word": row[1],
                "persian_word": row[2],
                "author": row[3]
            }
            for row in rows
        ]

    def english_word_exists(self, en_word):
        self._cursor.execute("SELECT 1 FROM dictionary_entries WHERE english_word = ?", (en_word,))
        return self._cursor.fetchone() is not None

    def get_fa_translations_by_en_word(self, en_word):
        self._cursor.execute("""
            SELECT d.persian_word, u.username
            FROM dictionary_entries d
            LEFT JOIN users u ON d.author_id = u.id
            WHERE d.english_word = ?
        """, (en_word,))
        rows = self._cursor.fetchall()
        return {row[0]: row[1] for row in rows}

    def persian_word_exists(self, fa_word):
        self._cursor.execute("SELECT 1 FROM dictionary_entries WHERE persian_word = ?", (fa_word,))
        return self._cursor.fetchone() is not None

    def get_en_translations_by_fa_word(self, fa_word):
        self._cursor.execute("""
            SELECT d.english_word, u.username
            FROM dictionary_entries d
            LEFT JOIN users u ON d.author_id = u.id
            WHERE d.persian_word = ?
        """, (fa_word,))
        rows = self._cursor.fetchall()
        return {row[0]: row[1] for row in rows}

    def insert_word(self, en_word, fa_word, author_username):
        self._cursor.execute("SELECT id FROM users WHERE username = ?", (author_username,))
        result = self._cursor.fetchone()
        if not result:
            raise Exception("[*][insert_word]Database error: author not found")
        author_id = result[0]
        self._cursor.execute("""
            INSERT INTO dictionary_entries (english_word, persian_word, author_id)
            VALUES (?, ?, ?)
        """, (en_word, fa_word, author_id))

    def author_has_words(self, author_username):
        self._cursor.execute("""
            SELECT 1
            FROM dictionary_entries d
            JOIN users u ON d.author_id = u.id
            WHERE u.username = ?
        """, (author_username,))
        return self._cursor.fetchone() is not None

    def word_id_belongs_to_author(self, word_id, author_username):
        self._cursor.execute("""
            SELECT 1
            FROM dictionary_entries d
            JOIN users u ON d.author_id = u.id
            WHERE d.id = ? AND u.username = ?
        """, (word_id, author_username))
        return self._cursor.fetchone() is not None

    def update_word_by_id(self, word_id, fields):
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
        values.append(word_id)
        self._cursor.execute(f"""
            UPDATE dictionary_entries
            SET {', '.join(updates)}
            WHERE id = ?
        """, values)

    def word_id_exists(self, word_id):
        self._cursor.execute("SELECT 1 FROM dictionary_entries WHERE id = ?", (word_id,))
        return self._cursor.fetchone() is not None

    def delete_word_by_id(self, word_id):
        self._cursor.execute("DELETE FROM dictionary_entries WHERE id = ?", (word_id,))
