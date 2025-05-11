from psycopg_pool import ConnectionPool
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
import psycopg

DB_CONFIG = {
    "dbname": "your_db",
    "user": "your_user",
    "password": "your_password",
    "host": "localhost"
}

pool = ConnectionPool(conninfo=f"dbname={DB_CONFIG['dbname']} user={DB_CONFIG['user']} "
                               f"password={DB_CONFIG['password']} host={DB_CONFIG['host']}")

@retry(
    stop=stop_after_attempt(5),
    wait=wait_fixed(2),
    retry=retry_if_exception_type(psycopg.OperationalError)
)
def get_connection():
    return pool.connection(timeout=5)

# '''
# Users Schema:
# user_id: String, Required, Unique
# email: String, Required, Unique
# username: String, Required, Unique
# password: String, Required
# created_at: Date, Required

# Plans Schema:
# plan_id: String, Required, Unique
# user_id: String, Required
# title: String, Required
# days: Int, Required
# created_at: Date, Required

# Tasks Schema:
# task_id: String, Required, Unique
# plan_id: String, Required
# day: Int, Required
# description: String, Required
# completed: Boolean, Required
# '''

def init_db():
    with get_connection as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id VARCHAR(255) NOT NULL PRIMARY KEY,
                email VARCHAR(255) NOT NULL UNIQUE,
                username VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                created_at DATETIME NOT NULL
            )
        ''')

        conn.execute('''
            CREATE TABLE IF NOT EXISTS plans (
                plan_id VARCHAR(255) NOT NULL PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,
                title VARCHAR(255) NOT NULL,
                days INT NOT NULL,
                created_at DATETIME NOT NULL
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')

        conn.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                task_id VARCHAR(255) NOT NULL PRIMARY KEY,
                plan_id VARCHAR(255) NOT NULL,
                day INT NOT NULL,
                description TEXT NOT NULL,
                completed BOOL NOT NULL
            )
        ''')

    if __name__ == "__main__":
        init_db()
