import os
import json
import sqlite3

# From: https://goo.gl/YzypOI
def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

class DB(object):
    """
    DB driver for the Todo app - deals with writing entities
    to the DB and reading entities from the DB
    """

    def __init__(self):
        self.conn = sqlite3.connect("todo.db", check_same_thread=False)
        self.create_post_table()
        self.create_comment_table()
        self.get_all_posts()
    

        # TODO - Create all other tables here

    def create_post_table(self):
        try:
            self.conn.execute("""
                CREATE TABLE posts
                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                SCORE INTEGER NOT NULL,
                TEXT TEXT NOT NULL,
                USERNAME TEXT NOT NULL);
                """)
        except Exception as e:
            print(e)

    def create_comment_table(self):
        try:
            self.conn.execute("""
                CREATE TABLE comment
                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                SCORE INTEGER NOT NULL,
                TEXT TEXT NOT NULL,
                USERNAME TEXT NOT NULL,
                POST_ID INTEGER NOT NULL);
                """)
        except Exception as y:
            print(y)


    def delete_post_table(self):
        self.conn.execute("""DROP TABLE IF EXISTS post;""")
    
    def get_all_posts(self):
        cursor = self.conn.execute("""
        SELECT * FROM posts;
        """)

        post=[]
        
        for row in cursor:
            post.append({
                'id': row[0],
                'score': row[1],
                'text': row[2],
                'username': row[3]
            })
        return post
        
    def create_post(self, text, username):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO posts (SCORE, TEXT, USERNAME) VALUES (?, ?, ?)', (0, text, username))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_post_by_id(self, post_id):
        cursor = self.conn.execute('SELECT * FROM posts WHERE id = ?', (post_id, ))
        for row in cursor:
            return {'id': row[0], 'score': row[1], 'text': row[2], 'username': row[3]}
        return None
    
    def edit_post_by_id(self, post_id, text):
        cursor = self.conn.execute("""
            UPDATE posts SET
            TEXT = ?
            WHERE id = ?""",(text, post_id, )
            )
        self.conn.commit()
        return self.get_post_by_id(post_id)
    
    def delete_post_by_id(self, post_id):
        cursor = self.conn.execute("""
            DELETE FROM posts
            WHERE id = ?""",(post_id, )
            )
        self.conn.commit()
        return self.get_post_by_id(post_id)
    
    def get_comment_by_id(self, post_id):
        cursor = self.conn.execute('SELECT * FROM comment WHERE post_id = ?', (post_id, ))
        """for row in cursor:
            return {'id': row[0], 'score': row[1], 'text': row[2], 'username': row[3], 'post_id': row[4]}
        return None"""

        comments=[]
        if cursor is not None:
            for row in cursor:
                comments.append({
                    'id': row[0],
                    'score': row[1],
                    'text': row[2],
                    'username': row[3],
                    'post_id': row[4]
                    })
            return comments
        return None

    def create_comment(self, text, username, post_id):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO comment (SCORE, TEXT, USERNAME, POST_ID) VALUES (?, ?, ?, ?)', (0, text, username, post_id ))
        self.conn.commit()
        return cursor.lastrowid
    
    

    def example_create_table(self):
        """
        Demonstrates how to make a table. Silently error-handles
        (try-except) because the table might already exist.
        """
        try:
            self.conn.execute("""
                CREATE TABLE example
                (ID INTEGER PRIMARY KEY NOT NULL,
                NAME TEXT NOT NULL,
                ADDRESS CHAR(50) NOT NULL);
            """)
        except Exception as e:
            print(e) 

    def example_query(self):
        """
        Demonstrates how to execute a query.
        """
        cursor = self.conn.execute("""
            SELECT * FROM example;
        """)

        for row in cursor:
            print("ID = ", row[0])
            print("NAME = ", row[1])
            print("ADDRESS = ", row[2], "\n")

    def example_insert(self):
        """
        Demonstrates how to perform an insert operation.
        """
        self.conn.execute("""
            INSERT INTO example (ID,NAME,ADDRESS)
            VALUES (1, "Joe", "Ithaca, NY");
        """)
        self.conn.commit()


# Only <=1 instance of the DB driver
# exists within the app at all times
DB = singleton(DB)
