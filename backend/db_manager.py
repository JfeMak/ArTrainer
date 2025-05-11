from db import get_connection

USER_SEQ = 100000000
PLANS_SEQ = 300000000
TASKS_SEQ = 500000000

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

class DbManager:
    def gen_user_uuid(self):
        return str(uuid.uuid1(node=uuid.getnode(), clock_seq=USER_SEQ))

    def gen_plan_uuid(self):
        return str(uuid.uuid1(node=uuid.getnode(), clock_seq=PLANS_SEQ))

    def gen_task_uuid(self):
        return str(uuid.uuid1(node=uuid.getnode(), clock_seq=TASKS_SEQ))

    # Users

    def create_user(self, email, username, password, created_at):
        user_id = self.gen_user_uuid()
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO users (user_id, email, username, password, created_at) VALUES (%s, %s, %s, %s, %s)",
                (user_id, email, username, password, created_at)
            )
            return self.get_user_by_id(user_id)

    def get_all_users(self):
        with get_connection() as conn:
            result = conn.execute("SELECT * FROM users")
            columns = result.keys()
            rows = result.fetchall()
            return [dict(zip(columns, row)) for row in rows]

    def get_user_by_id(self, user_id):
        with get_connection() as conn:
            result = conn.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            return result.mappings().fetchone()

    # Plans

    def create_plan(self, user_id, title, days, created_at):
        plan_id = self.gen_plan_uuid()
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO plans (plan_id, user_id, title, days, created_at) VALUES (%s, %s, %s, %s, %s)",
                (plan_id, user_id, title, days, created_at)
            )
            return self.get_plan_by_id(plan_id)

    def get_plans_by_user_id(self, user_id):
        with get_connection() as conn:
            result = conn.execute("SELECT * FROM plans WHERE user_id = %s", (user_id,))

    def get_plan_by_id(self, plan_id):
        with get_connection() as conn:
            result = conn.execute("SELECT * FROM plans WHERE plan_id = %s", (plan_id,))
            return result.mappings().fetchone()

    # Tasks

    def create_task(self, plan_id, day, description):
        task_id = self.gen_task_uuid()
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO tasks (task_id, plan_id, day, description, completed) VALUES (%s, %s, %s, %s, %s)",
                (task_id, plan_id, day, description, False)
            )
            return self.get_task_by_id(task_id)

    def get_tasks_by_plan_id(self, plan_id):
        with get_connection() as conn:
            result = conn.execute(
                "SELECT * FROM tasks WHERE plan_id = %s",
                (plan_id,)
            )
            return result.mappings().fetchall()

    def get_task_by_id(self, task_id):
        with get_connection() as conn:
            result = conn.execute("SELECT * FROM tasks WHERE task_id = %s", (task_id,))
            return result.mappings().fetchone()

    def complete_task(self, task_id):
        with get_connection() as conn:
            conn.execute("UPDATE tasks SET completed = TRUE WHERE task_id = %s", (task_id,))
            return None
