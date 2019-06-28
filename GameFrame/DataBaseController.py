import os
import sqlite3


class DataBaseController:
    def __init__(self, dbase_file_name: str):
        app_file_path = os.path.join(os.path.dirname(__file__), dbase_file_name)
        self.app_db = sqlite3.connect(app_file_path)
        self.app_cursor = self.app_db.cursor()

    def close(self):
        self.app_db.close()

    # ------------------------------ #
    # -- This is an example query -- #
    # ------------------------------ #
'''
    def get_lesson(self, topic):
        self.app_cursor.execute(
            """
                SELECT lesson
                FROM Topic
                WHERE name = :topic
            """,
            {'topic': topic}
        )
        return self.app_cursor.fetchone()[0]
'''
