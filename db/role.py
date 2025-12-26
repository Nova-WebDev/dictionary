class RoleRepository:
    def __init__(self, cursor):
        self._cursor = cursor

    def get_all_roles(self):
        self._cursor.execute("SELECT id, role_name FROM roles")
        rows = self._cursor.fetchall()
        return [{"id": row[0], "role_name": row[1]} for row in rows]

    def role_id_exists(self, role_id):
        self._cursor.execute("SELECT 1 FROM roles WHERE id = ?", (role_id,))
        return self._cursor.fetchone() is not None

    def get_role_name_by_id(self, role_id):
        self._cursor.execute("SELECT role_name FROM roles WHERE id = ?", (role_id,))
        result = self._cursor.fetchone()
        if not result:
            raise Exception("[*][get_role_name_by_id]Database error: role_id not found in roles table")
        return result[0]
