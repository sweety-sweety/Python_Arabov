import sqlite3
from datetime import datetime
from typing import Optional

DB_FILENAME = "tasks.db"


def get_conn(db_path: Optional[str] = None):
    if db_path:
        return sqlite3.connect(db_path)
    return sqlite3.connect(DB_FILENAME)


def init_db(db_path: Optional[str] = None):
    with get_conn(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                created_at TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        conn.commit()


def add_task(description: str, db_path: Optional[str] = None):
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_conn(db_path) as conn:
        conn.execute(
            "INSERT INTO tasks (description, created_at, done) VALUES (?, ?, ?)",
            (description, created_at, 0),
        )
        conn.commit()


def mark_done(task_id: int, db_path: Optional[str] = None):
    with get_conn(db_path) as conn:
        cur = conn.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
        if cur.rowcount == 0:
            raise ValueError("Задача с таким ID не найдена")
        conn.commit()


def delete_task(task_id: int, db_path: Optional[str] = None):
    with get_conn(db_path) as conn:
        cur = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        if cur.rowcount == 0:
            raise ValueError("Задача с таким ID не найдена")
        conn.commit()


def fetch_all(db_path: Optional[str] = None):
    with get_conn(db_path) as conn:
        return conn.execute(
            "SELECT id, description, created_at, done FROM tasks ORDER BY id DESC"
        ).fetchall()


def print_tasks(tasks):
    if not tasks:
        print("Список задач пуст.")
        return
    print("\nСписок задач:")
    print("=" * 50)
    for task in tasks:
        id_, desc, created, done = task
        status = "[x]" if done else "[ ]"
        print(f"{id_:<3} {status} {desc} (создана {created})")
    print()


def main_menu():
    print("""
===== Менеджер задач =====
1. Добавить задачу
2. Отметить задачу как выполненную
3. Удалить задачу
4. Показать все задачи
0. Выход
""")


def main(db_path: Optional[str] = None):
    init_db(db_path)
    while True:
        main_menu()
        choice = input("Выберите пункт: ").strip()
        try:
            if choice == "1":
                desc = input("Введите описание задачи: ").strip()
                if desc:
                    add_task(desc, db_path)
                    print("Задача добавлена.")
                else:
                    print("Описание не может быть пустым.")

            elif choice == "2":
                task_id = int(input("Введите ID задачи для отметки: ").strip())
                mark_done(task_id, db_path)
                print("Задача отмечена как выполненная.")

            elif choice == "3":
                task_id = int(input("Введите ID задачи для удаления: ").strip())
                delete_task(task_id, db_path)
                print("Задача удалена.")

            elif choice == "4":
                tasks = fetch_all(db_path)
                print_tasks(tasks)

            elif choice == "0":
                print("Выход.")
                break

            else:
                print("Неверный пункт меню.")
        except Exception as e:
            print("Ошибка:", e)


if __name__ == "__main__":
    main()