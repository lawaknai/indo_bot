import sqlite3

class DatabaseManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def get_content(self, data):
        query = "SELECT content_type, file_id, from_id FROM data WHERE short_token = ? LIMIT 1"
        self.cursor.execute(query, data)
        result = self.cursor.fetchone()
        return result

    def insert_data(self, data):
        query = "INSERT INTO user (user_id, first_name, last_name, username, file_id) VALUES (?, ?, ?, ?, ?)"
        self.cursor.execute(query, data)
        self.connection.commit()
        
    def insert_content(self, data):
        query = "INSERT INTO data (content_type, short_token, file_id, from_id) VALUES (?, ?, ?, ?)"
        self.cursor.execute(query, data)
        self.connection.commit()

    def close_connection(self):
        self.cursor.close()
        self.connection.close()
