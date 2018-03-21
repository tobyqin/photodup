import sqlite3

db_file = "photo.db"
conn = sqlite3.connect(db_file)
cursor = conn.cursor()


def create_table():
    drop_table()
    cursor.execute('''CREATE TABLE photo (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    hash VARCHAR(50) NOT NULL,
                    name TEXT NOT NULL,
                    path TEXT NOT NULL,
                    existed INTEGER DEFAULT 1)''')


def drop_table():
    cursor.execute('DROP TABLE IF EXISTS photo')


def insert_file(hash, name, path):
    cursor.execute('INSERT INTO photo (hash,name,path) VALUES (?,?,?)', (hash, name, path))


def is_existed(file_path):
    cursor.execute('SELECT COUNT(*) FROM photo WHERE path = ?', (file_path,))
    row = cursor.fetchone()
    return row[0] != 0


def mark_deleted(file_path):
    cursor.execute('UPDATE photo SET existed =0 WHERE NAME = ?', (file_path,))
    conn.commit()


def find_duplicate():
    cursor.execute('''SELECT * FROM photo WHERE hash IN
                      (SELECT hash FROM photo GROUP BY hash HAVING count(*) > 1)''')
    rows = cursor.fetchall()
    return rows


def close_db():
    if conn is not None:
        conn.close()


if __name__ == '__main__':
    print('create photo.db ...')
    create_table()
    close_db()
    print('done!')
